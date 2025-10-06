import streamlit as st
import json

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>About - JSON-LD Schema</h1>"
st.html(title_alignment)

# --- Overview ---------------------------------------------------------------
st.markdown("""
## Overview

This application implements the **four-entity conceptual map** for the LLM ecosystem - **Model, Dataset, Task, Metric** - and their **six binary relationships** (e.g., *trained_on*, *tested_on*, *suited_for*, *enabled_by*, *evaluates_model*, *assesses*).  

### Architecture

Two storage implementations:
- **JSON** (demo): Simple JSON files stored in local. 
- **MongoDB** (scalable): with one collection per entity and an **Edges** collection

Both implementations follow the same JSON-LD schema principles with consistent data structures.
""")

st.markdown("---")

# --- Entity Types -----------------------------------------------------------
st.markdown("## Entity Types")

# Models
st.markdown("### Model")
st.markdown("""
**Schema Structure (example):**
""")

model_example = {
    "_id": "model:meta-llama/Llama-3.2-3B",
    "Name": "Llama",
    "Version": "3.2-3B",
    "URI": "https://huggingface.co/meta-llama/Llama-3.2-3B",
    "LicenseToUse": "llama3.2",
    "ModelCreator": "Meta",
    "Developer": "meta-llama",
    "OpenSource": True,                          # paper notes the platform tag nuance
    "CarbonEmissions": 240,                      # tCO2e when available
    "LibraryFramework": "PyTorch",
    "Language": ["English", "German", "French"],
    "Architecture": "Transformer",
    "NumberOfParameters": "3B",
    "ContextLength": "128k tokens",
    "Tokenization": "BPE",
    "NumberOfTokens": "128k",
    "Quantization": False,
    "InstructionTuned": True,
    "HumanAligned": True
}
st.json(model_example)

st.markdown("""
**Key Fields:**
- `Name` + `Version` are the identifier pair; `URI`, `LicenseToUse`, `ModelCreator`, `Developer`, `OpenSource`, `CarbonEmissions` support **FAIR** and transparency.
- Implementation: `LibraryFramework`, `Language`, `Architecture`, `NumberOfParameters`, `ContextLength`, `Tokenization`, `NumberOfTokens`, `Quantization`, `InstructionTuned`, `HumanAligned`.
""")

# Datasets
st.markdown("### Dataset")
st.markdown("""
**Schema Structure (example):**
""")

dataset_example = {
    "_id": "dataset:IMDB-Reviews",
    "Name": "IMDB Reviews",
    "URI": "https://ai.stanford.edu/~amaas/data/sentiment/",
    "LicenseToUse": "other",
    "Domain": ["Reviews"],
    "Size": "50k",
    "Language": ["English"],
    "FineTuning": True,
    "Annotation": {
        "type": "supervised",
        "who": "Domain experts"
    }
}
st.json(dataset_example)

st.markdown("""
**Key Fields:**
- `Name`, `URI`, `LicenseToUse`, `Domain`, `Size`, `Language`, `FineTuning`, `Annotation`
""")

# Tasks
st.markdown("### Task")
st.markdown("""
**Schema Structure (example):**
""")

task_example = {
    "_id": "task:sentiment-analysis",
    "Name": "Sentiment Analysis",
    "Description": "Determines the sentiment of a given text",
    "SubTask": ["Emotion Detection"]
}
st.json(task_example)

st.markdown("""
**Key Fields:** `Name`, `Description`, `SubTask`.
""")

# Metrics
st.markdown("### Metric")
st.markdown("""
**Schema Structure (example):**
""")

metric_example = {
    "_id": "metric:BLEU",
    "Name": "BLEU",
    "Description": "Assess goodness of translation",
    "ContextFree": True,
    "Trained": False,
    "FeatureBased": False,
    "Granularity": ["SentenceLevel"]
}
st.json(metric_example)

st.markdown("""
**Key Fields:** `ContextFree`, `Trained`, `FeatureBased`, `Granularity` (e.g., Word-Character, Embeddings, SentenceLevel).
""")

st.markdown("---")

# --- Relationships (Edges) --------------------------------------------------
st.markdown("## Relationships (Edges)")

st.markdown("""
The six binary relations connecting entities are explicitly typed and directed.

**Schema Structure (example):**
""")

edge_example = {
    "_id": "edge:sf:deepseek-codegen",
    "relation_type": "suited_for",
    "from": "model:deepseek-ai/deepseek-coder-6.7b-instruct",
    "to": "task:code-generation"
}
st.json(edge_example)

st.markdown("### Relationship Types")
relationships = [
    {
        "type": "suited_for",
        "description": "Model → Task (a model is suitable for a task)",
        "example": "model:deepseek-ai/deepseek-coder-6.7b-instruct → task:code-generation"
    },
    {
        "type": "trained_on",
        "description": "Model → Dataset",
        "example": "model:FinGPT/fingpt-llama3-8b-lora → dataset:FinQA"
    },
    {
        "type": "tested_on",
        "description": "Model → Dataset",
        "example": "model:epfl-llm/meditron-7b → dataset:MMLU-Clinical"
    },
    {
        "type": "evaluates_model",
        "description": "Metric → Model (includes score)",
        "example": "metric:Tabby → model:deepseek-ai/deepseek-coder-6.7b-instruct (score: 42.36)"
    },
    {
        "type": "assesses_task",
        "description": "Metric → Task (metric is designed to assess a task)",
        "example": "metric:Tabby → task:code-generation"
    },
    {
        "type": "enabled_by",
        "description": "Task → Dataset (dataset enables the task)",
        "example": "task:code-generation → dataset:HumanEval"
    }
]
for rel in relationships:
    st.markdown(f"**`{rel['type']}`**: {rel['description']}")
    st.markdown(f"*Example: {rel['example']}*")
    st.markdown("")

st.markdown("---")
