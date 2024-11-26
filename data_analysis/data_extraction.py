from huggingface_hub import HfApi
import pandas as pd
import itertools
import re
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from huggingface_hub.utils import logging

from tags import * # tags.py
logging.set_verbosity_error()

# Pattern matching functions

def extract_name(full_name):
    pattern = re.compile(r'[^/]+/(.+)')
    match = re.search(pattern, full_name)
    if match:
        return match.group(1) # the part after '/' might also contain version and number of parameters (impossible to extract in a uniform way)
    else:
        return full_name

def match_string(entries, pattern):
    pattern = re.compile(pattern)
    for entry in entries:
        match = pattern.match(entry)
        if match:
            return match.group(1)
    return None

def find_all_matches(entries, pattern):
    pattern = re.compile(pattern)
    matches = []
    for entry in entries:
        match = pattern.match(entry)
        if match:
            matches.append(match.group(1))
    return matches

def match_license(entries):
    return match_string(entries, r'license:(\S+)')

def match_dataset(entries):
    return find_all_matches(entries, r'dataset:(\S+)')

def match_uri(entries):
    uri = match_string(entries, r'arxiv:(\S+)')
    if uri is None:
        uri = match_string(entries, r'doi:(\S+)')
    return uri

def match_language(entries):
    return find_all_matches(entries, r'language:(\S+)')

def match_size(entries):
    return match_string(entries, r'size_categories:(\S+)')

def match_tasks(entries):
    return find_all_matches(entries, r'task_categories:(\S+)')

def add_to_json_file(data, file_path):

    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as f:

            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)
            f.truncate()
            f.write(',\n')
            json.dump(data, f, indent=4)
            f.write(']')
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([data], f, indent=4)

def extract_model_attributes(model):

	model_tags = model.tags
	if model.card_data is not None:
		model_card_data = model.card_data.to_dict()
	else:
		model_card_data = None
	model_attributes = dict()

	model_attributes['name'] = extract_name(model.id)
	model_attributes['id'] = model.id
	model_attributes['version'] = None # sometimes in model['id'] but impossible to extract in a uniform way
	model_attributes['numberOfParameters'] = None # sometimes in model['id'] or model description but impossible to extract in a uniform way

	model_attributes['quantization'] = None
	for t in model_tags:
		if t in tag_quantization:
			model_attributes['quantization'] = t

	model_attributes['architecture'] = None
	try:
		if model_card_data is not None:
			model_attributes['architecture'] = model_card_data['base_model']
	except KeyError:
		pass

	model_attributes['languages'] = []
	for t in model_tags:
		if t in tag_language:
			model_attributes['languages'].append(t)

	model_attributes['modelCreator'] = None # extracted in a postprocessing step

	model_attributes['licenseToUse'] = match_license(model_tags)

	model_attributes['libraryFramework'] = [] 
	for t in model_tags:
		if t in tag_library:
			model_attributes['libraryFramework'].append(t)

	model_attributes['contextLength'] = None
	model_attributes['developers'] = [model.author]
	model_attributes['openSource'] = True

	model_attributes['uri'] = match_uri(model_tags)

	model_attributes['fineTuned'] = None # if there is a 'base_model' in card_data, it is fine-tuned
	try:
		if model_card_data is not None:
			if 'base_model' in model_card_data:
				model_attributes['fineTuned'] = True
	except KeyError:
		pass

	model_attributes['carbonEmission [CO2eq tons]'] = None
	try:
		if model_card_data is not None:
			model_attributes['carbonEmission [CO2eq tons]'] = model_card_data['co2_eq_emissions']
	except KeyError:
		pass

	model_attributes['tokenizer'] = None
	model_attributes['likes'] = model.likes

	info = api.model_info(repo_id=model.id, expand="downloadsAllTime")
	model_attributes['downloads_all_time'] = int(info.downloads_all_time)

	model_attributes['downloads'] = model.downloads

	model_attributes['creation_date'] = model.created_at.strftime('%Y-%m-%d %H:%M:%S')


	return model_attributes

if __name__ == "__main__":
    api = HfApi()

    # Scrape languages from HF

    url_languages = 'https://huggingface.co/languages'

    response = requests.get(url_languages)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    code_tags = soup.find_all('code')
    tag_language = [code_tag.get_text() for code_tag in code_tags]

    tag_language.remove('jax') # 'jax' is the ISO for Jambi Malay (present in 3 datasets, 36 models), impossible to distinguish from JAX the library... TODO: better solution?

    tag_language = set(tag_language)

    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    result_path = os.path.join(parent_path, 'database', 'HF entries', 'hf extracted json')
    os.makedirs(result_path, exist_ok=True)

    file_path = os.path.join(result_path, 'models_duplicates_no_modelCreator.json')

    # Total: 697,162 models
    count = 0
    start_time = time.time()
    for task in TAG_DOWNSTREAM_TASK:
        print(f'Processing {task} models...')
        models = api.list_models(filter=task, full=True, cardData=True)
        for model in models:
            model_attributes = extract_model_attributes(model)
            add_to_json_file(model_attributes, file_path)
            count += 1
            if count % 1000 == 0:
                print(f'{count} models processed, {time.time() - start_time} seconds elapsed')
            if count == 200000:
                break
    
    for task in TAG_DOWNSTREAM_TASK:
        print(f'Processing {task} models...')
        models = api.list_models(filter=task, full=True, cardData=True)
        for model in models:
            model_attributes = extract_model_attributes(model)
            add_to_json_file(model_attributes, "text")
            count += 1
            if count % 1000 == 0:
                print(f'{count} models processed, {time.time() - start_time} seconds elapsed')
    
    file_path = os.path.join(result_path, 'models_duplicates_no_modelCreator.json')

    with open(file_path, 'r') as file:
        data = json.load(file)
    models_df = pd.DataFrame(data)

    # Remove duplicates
    print(f'len before removing duplicates: {  len(models_df) }')
    models_df = models_df.loc[models_df.astype(str).drop_duplicates().index]
    print(f'len after removing duplicates: {  len(models_df) }')

    # Postprocessing: find the modelCreator

    df_filtered = models_df[models_df['architecture'].notna()]

    # Process each row
    count = 0
    start_time = time.time()
    for index, row in df_filtered.iterrows():
        # Find the row where 'id' matches the 'architecture' of the current row
        try:
            matching_row = models_df[models_df['id'].astype(str) == str(row['architecture'])]
        except ValueError:
            break
        
        if not matching_row.empty:
            # Get the first developer from the 'developers' list
            first_developer = matching_row['developers'].iloc[0][0] if matching_row['developers'].iloc[0] else None
            # Set the 'modelCreator' attribute of the original row
            models_df.at[index, 'modelCreator'] = first_developer
        
        count += 1
        if count % 1000 == 0:
            print(f'{count} rows processed ({count/len(df_filtered)*100} %), elapsed time: {time.time() - start_time} seconds, estimated time remaining: {(time.time() - start_time) / count * (len(df_filtered) - count)} seconds')
        
    
    models_list = models_df.drop(columns=['id']).to_dict(orient='records')

    file_path_postprocessed = os.path.join(result_path, 'models.json')

    with open(file_path_postprocessed, "w") as json_file:
        json.dump(models_list, json_file, indent=4)