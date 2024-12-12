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

api = HfApi()

# Scrape languages from HF

url_languages = 'https://huggingface.co/languages'

default_path = "/home/csavelli/database/HF entries/hf extracted json/"

response = requests.get(url_languages)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

code_tags = soup.find_all('code')
tag_language = [code_tag.get_text() for code_tag in code_tags]

tag_language.remove('jax') # 'jax' is the ISO for Jambi Malay (present in 3 datasets, 36 models), impossible to distinguish from JAX the library... TODO: better solution?

tag_language = set(tag_language)

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

current_path = os.getcwd()
parent_path = os.path.dirname(current_path)
result_path = os.path.join(parent_path, 'database', 'HF entries', 'hf extracted json')
os.makedirs(result_path, exist_ok=True)

# load llm json 

with open('/home/csavelli/chatIMPACT/database/database/HF entries/hf extracted json/models.json', 'r') as f:
    llm = json.load(f)

models_df = pd.DataFrame(llm)

from huggingface_hub import HfApi
import requests
from requests.exceptions import RequestException
import json
import time

def get_model_vocab_size(model_id):
    """
    Get the vocabulary size of a model without downloading the full tokenizer
    
    Parameters:
    model_id (str): The Hugging Face model ID (e.g., 'bert-base-uncased')
    
    Returns:
    int or None: Vocabulary size if found, None otherwise
    """
    # Clean up model ID
    model_id = model_id.strip('/')
    
    def get_json_from_url(url):
        try:
            headers = {
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if the response is valid JSON
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return None
            return None
        except RequestException:
            return None

    # List of possible config file locations
    config_files = [
        f"https://huggingface.co/{model_id}/raw/main/config.json",
        f"https://huggingface.co/{model_id}/resolve/main/config.json",
        f"https://huggingface.co/{model_id}/raw/master/config.json",
        f"https://huggingface.co/{model_id}/raw/main/tokenizer_config.json",
        f"https://huggingface.co/{model_id}/resolve/main/tokenizer_config.json",
        f"https://huggingface.co/{model_id}/raw/master/tokenizer_config.json"
    ]

    # Try each config file location
    for config_url in config_files:
        config = get_json_from_url(config_url)
        if config:
            # Check various possible vocabulary size keys
            for key in ['vocab_size', 'n_vocab', 'tokenizer_vocab_size']:
                if key in config:
                    return config[key]
    
    return None

vocab_size = []

for i, row in enumerate(models_df.iterrows()):
    model_id = row[1]['id']
    print(f"Processing model {i+1}/{len(models_df)}: {model_id}")
    try:
        vocab_size.append(get_model_vocab_size(model_id))
    except:
        vocab_size.append(None)

import pickle

with open('/home/csavelli/chatIMPACT/database/database/HF entries/hf extracted json/vocab_size.pkl', 'wb') as f:
    pickle.dump(vocab_size, f)