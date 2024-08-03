#######
# LLM #
#######

tag_quantization = ['4-bit','8-bit']

tag_architecture = []

# language = [] # scraped from https://huggingface.co/languages (see .ipynb)

# 'license:apache-2.0'
tag_license_to_use = ['apache-2.0','mit','openrail','creativeml-openrail-m','other','cc-by-nc-4.0','llama2','cc-by-4.0','llama3','openrail++',
					  'afl-3.0','cc-by-nc-sa-4.0','gpl-3.0','cc-by-sa-4.0','gemma','cc','artistic-2.0','bsd-3-clause','bigscience-openrail-m',
					  'bigscience-bloom-rail-1.0','cc-by-nc-nd-4.0','bigcode-openrail-m','wtfpl','agpl-3.0','llama3.1','cc0-1.0','unlicense',
					  'cc-by-sa-3.0','gpl','bsd','cc-by-nc-2.0','cc-by-3.0','cc-by-2.0','gpl-2.0','lgpl-3.0','bsl-1.0','c-uda','bsd-2-clause',
					  'osl-3.0','cc-by-nd-4.0','cdla-permissive-2.0','cc-by-nc-3.0','ms-pl','pddl','ecl-2.0','gfdl','bsd-3-clause-clear',
					  'cc-by-nc-nd-3.0','zlib','mpl-2.0','odbl','cc-by-nc-sa-3.0','cc-by-nc-sa-2.0','lgpl','deepfloyd-if-license','lgpl-2.1',
					  'odc-by','epl-2.0','lgpl-lr','cc-by-2.5','eupl-1.1','isc','ncsa','etalab-2.0','cdla-sharing-1.0','postgresql','lppl-1.3c',
					  'epl-1.0','apple-ascl','ofl-1.1','cdla-permissive-1.0']

# TODO: check if correct -> does program languages like rust count as a domain?
tag_library = ['pytorch','tf','jax','transformers','safetensors','tensorboard','peft','diffusers','gguf','stable-baselines3','onnx',
			   'sentence-transformers','ml-agents','tf-keras','adapters','setfit','timm','sample-factory','flair','keras','mlx',
			   'transformers.js','spacy','fastai','espnet','openvino','core-ml','nemo','joblib','rust','bertopic','tf-lite','openclip',
			   'fasttext','scikit-learn','speechbrain','paddlepaddle','fairseq','graphcore','asteroid','llamafile','allennlp','stanza',
			   'spanmarker','paddlenlp','habana','pyannote.audio','pythae','unity-sentis']

tag_carbon_emission = ['co2_eq_emissions'] # boolean... TODO: where are the values? -> https://huggingface.co/blog/carbon-emissions-on-the-hub but can't retrieve the models like in the example

TAG_DOWNSTREAM_TASK = ['text-classification','token-classification','table-question-answering','question-answering','zero-shot-classification',
				   'translation','summarization','feature-extraction','text-generation','text2text-generation','fill-mask','sentence-similarity']

# 'dataset:openslr'
# TAG_DATASET = []

###########
# Dataset #
###########

# tag_license_to_use = [] # see LLM

# tag_language = [] # see LLM

# 'size_categories:10K<n<100K'
# tag_size = []

# TODO: check if complete (how?) -> in HF dataset page these are the only available (so retrievable in an automated way)
tag_domain = ['art','code','medical','legal','finance','biology','music','chemistry','climate','Synthetic']

# 'task_categories:question-answering'
# TAG_DOWNSTREAM_TASK = [] # see LLM

##########
# Metric #
##########

###################
# Downstream task #
###################
