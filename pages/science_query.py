import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Science"
MODELS = "Models"
DATASETS = "Datasets"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

# Initialize session state with default values to prevent KeyError
if f"{PAGE}.num_param_filter" not in st.session_state:
    st.session_state[f"{PAGE}.num_param_filter"] = "No filters"
if f"{PAGE}.min_num_param" not in st.session_state:
    st.session_state[f"{PAGE}.min_num_param"] = 0.0
if f"{PAGE}.max_num_param" not in st.session_state:
    st.session_state[f"{PAGE}.max_num_param"] = 1000.0
if f"{PAGE}.open_source" not in st.session_state:
    st.session_state[f"{PAGE}.open_source"] = "True"
if f"{PAGE}.instruction_tuned" not in st.session_state:
    st.session_state[f"{PAGE}.instruction_tuned"] = "No filter"
if f"{PAGE}.carbon_filter" not in st.session_state:
    st.session_state[f"{PAGE}.carbon_filter"] = "No filters"
if f"{PAGE}.min_carbon" not in st.session_state:
    st.session_state[f"{PAGE}.min_carbon"] = 0.0
if f"{PAGE}.max_carbon" not in st.session_state:
    st.session_state[f"{PAGE}.max_carbon"] = 10000.0
if f"{PAGE}.lan_llm" not in st.session_state:
    st.session_state[f"{PAGE}.lan_llm"] = []
if f"{PAGE}.license" not in st.session_state:
    st.session_state[f"{PAGE}.license"] = ["apache-2.0"]
if f"{PAGE}.type_filter" not in st.session_state:
    st.session_state[f"{PAGE}.type_filter"] = "No filters"
if f"{PAGE}.min_size_rows" not in st.session_state:
    st.session_state[f"{PAGE}.min_size_rows"] = 0
if f"{PAGE}.max_size_rows" not in st.session_state:
    st.session_state[f"{PAGE}.max_size_rows"] = 1000000000
if f"{PAGE}.fine_tuning" not in st.session_state:
    st.session_state[f"{PAGE}.fine_tuning"] = "No filter"
if f"{PAGE}.domain" not in st.session_state:
    st.session_state[f"{PAGE}.domain"] = ["Mathematics", "Chemistry", "Physics"]
if f"{PAGE}.lan_ds" not in st.session_state:
    st.session_state[f"{PAGE}.lan_ds"] = []
if f"{PAGE}.lic" not in st.session_state:
    st.session_state[f"{PAGE}.lic"] = []
if f"{PAGE}.project_llm_multiselect" not in st.session_state:
    st.session_state[f"{PAGE}.project_llm_multiselect"] = ["name", "version", "numberOfParameters"]
if f"{PAGE}.project_ds_multiselect" not in st.session_state:
    st.session_state[f"{PAGE}.project_ds_multiselect"] = ["name", "uri", "domain"]
if f"{PAGE}.rank_by" not in st.session_state:
    st.session_state[f"{PAGE}.rank_by"] = "No ranking"
if f"{PAGE}.sort_order" not in st.session_state:
    st.session_state[f"{PAGE}.sort_order"] = "Descending (High to Low)"

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"
st.html(title_alignment)
st.image("static/4.png", use_column_width=True)

st.markdown("""
**Pre-configured Query:** *"Find Apache 2.0 licensed models trained on datasets covering all science domains (Mathematics, Chemistry, AND Physics)."*

This query considers the **Train** relationship between the **Model** and **Dataset** entities with the following pre-configured filters:
            
- **Model filters:** OpenSource=True, LicenseToUse=Apache-2.0  
- **Dataset filters:** Domain = Mathematics OR Chemistry OR Physics  
            
The filters are already applied in the sections below.
""")

# -----------------------------------------------------------------------------
# SECTION FOR LARGE LANGUAGE MODEL FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html("<h3 style='text-align: center;'>Large Language Model filters</h3>")
col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
)

with col_1:
    # vertical divider for spacing
    st.html(
        """
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            """
    )

with col_2:
    st.radio(
        "***Filter on Number of Parameters***",
        ["No filters", "Number of Parameters (B)"],
        key=f"{PAGE}.num_param_filter",
    )
    if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
        st.number_input(
            "**Minimum number of parameters (B)**", min_value=0.0, value=0.0, step=0.1,
            key=f"{PAGE}.min_num_param",
        )
        st.number_input(
            "**Maximum number of parameters (B)**", min_value=0.0, value=1000.0, step=0.1,
            key=f"{PAGE}.max_num_param",
        )

with col_3:
    st.html(
        """
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            """
    )

with col_4:
    # radio buttons for binary model attributes
    st.radio("**Open Source**", ["No filter", "True", "False"], 
             index=1, key=f"{PAGE}.open_source")  # Pre-set to True
    st.radio("**Instruction Tuned**", ["No filter", "True", "False"], 
             index=0, key=f"{PAGE}.instruction_tuned")
    st.radio(
        "***Filter on Carbon Emissions***",
        ["No filters", "Carbon Emissions (tCO2e)"],
        key=f"{PAGE}.carbon_filter",
    )
    if st.session_state[f"{PAGE}.carbon_filter"] == "Carbon Emissions (tCO2e)":
        st.number_input(
            "**Minimum emissions (tCO2e)**", min_value=0.0, value=0.0, step=0.1,
            key=f"{PAGE}.min_carbon",
        )
        st.number_input(
            "**Maximum emissions (tCO2e)**", min_value=0.0, value=10000.0, step=0.1,
            key=f"{PAGE}.max_carbon",
        )

with col_5:
    st.html(
        """
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        """
    )

with col_6:
    # multi‑select fields for categorical attributes
    st.multiselect(
        "**Language**",
        dao.get_all("Models", "languages"),
        key=f"{PAGE}.lan_llm",
        default=st.session_state.get(f"{PAGE}.lan_llm", []),
    )
    st.multiselect(
        "**License to Use**",
        dao.get_all("Models", "license_to_use"),
        key=f"{PAGE}.license",
        default=st.session_state.get(f"{PAGE}.license", ["apache-2.0"]),  # Pre-configured for Apache 2.0
    )

with col_7:
    st.html(
        """
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        """
    )

# Initialise filters for LLMs
st.session_state[f"{PAGE}.filters_llm"] = {}

# Add openSource filter only if not "No filter"
if st.session_state[f"{PAGE}.open_source"] != "No filter":
    st.session_state[f"{PAGE}.filters_llm"]["openSource"] = st.session_state[f"{PAGE}.open_source"] == "True"

# Add instructionTuned filter only if not "No filter"
if st.session_state[f"{PAGE}.instruction_tuned"] != "No filter":
    st.session_state[f"{PAGE}.filters_llm"]["instructionTuned"] = st.session_state[f"{PAGE}.instruction_tuned"] == "True"

# State flags for additional manual filtering (on numeric/string fields)
st.session_state[f"{PAGE}.param_filter_active"] = False
st.session_state[f"{PAGE}.carbon_filter_active"] = False

# Handle number of parameters filter
if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
    # When using numeric filters on a string field (e.g. "7B"), we can't rely on
    # MongoDB's comparison semantics. Instead, we store the bounds in the session
    # state and perform the comparison after retrieving the results.
    min_params = st.session_state[f"{PAGE}.min_num_param"]
    # If the user leaves the max field empty, treat it as a large upper bound
    max_params = (
        st.session_state[f"{PAGE}.max_num_param"]
        if st.session_state[f"{PAGE}.max_num_param"]
        else 1e9
    )
    st.session_state[f"{PAGE}.param_filter_active"] = True
    st.session_state[f"{PAGE}.min_params"] = min_params
    st.session_state[f"{PAGE}.max_params"] = max_params

# Handle carbon emissions filter
if st.session_state[f"{PAGE}.carbon_filter"] == "Carbon Emissions (tCO2e)":
    min_carbon = st.session_state[f"{PAGE}.min_carbon"]
    max_carbon = (
        st.session_state[f"{PAGE}.max_carbon"]
        if st.session_state[f"{PAGE}.max_carbon"]
        else 1e9
    )
    st.session_state[f"{PAGE}.carbon_filter_active"] = True
    st.session_state[f"{PAGE}.min_carbon_val"] = min_carbon
    st.session_state[f"{PAGE}.max_carbon_val"] = max_carbon

# Add language and license filters if set
if st.session_state[f"{PAGE}.lan_llm"]:
    st.session_state[f"{PAGE}.filters_llm"]["languages"] = {
        "$all": st.session_state[f"{PAGE}.lan_llm"]
    }

if st.session_state[f"{PAGE}.license"]:
    st.session_state[f"{PAGE}.filters_llm"]["license_to_use"] = {
        "$all": st.session_state[f"{PAGE}.license"]
    }

# -----------------------------------------------------------------------------
# SECTION FOR DATASET FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html("<h3 style='text-align: center;'>Dataset filters</h3>")
col_9, col_10, col_11, col_12, col_13, col_14, col_15, col_16 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
)

with col_9:
    st.html(
        """
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            """
    )

with col_10:
    st.radio(
        "***Filter on Dataset size***",
        ["No filters", "Row count"],
        key=f"{PAGE}.type_filter",
    )
    if st.session_state[f"{PAGE}.type_filter"] == "Row count":
        st.number_input(
            "**Minimum size [rows]**", min_value=0, value=0, key=f"{PAGE}.min_size_rows"
        )
        st.number_input(
            "**Maximum size [rows]**", min_value=0, value=1000000000,
            key=f"{PAGE}.max_size_rows",
        )

with col_11:
    st.html(
        """
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            """
    )

with col_12:
    # radio button to indicate whether a dataset is used for fine-tuning
    st.radio("**Fine-Tuning Dataset**", ["No filter", "True", "False"], 
             index=0, key=f"{PAGE}.fine_tuning")
    # domain selection - pre-configured for science domains
    st.multiselect(
        "**Domain**",
        dao.get_all("Datasets", "domain"),
        key=f"{PAGE}.domain",
        default=st.session_state.get(f"{PAGE}.domain", ["Mathematics", "Chemistry", "Physics"]),
    )

with col_13:
    st.html(
        """
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        """
    )

with col_14:
    # language and license filters for datasets
    st.multiselect(
        "**Language**",
        dao.get_all("Datasets", "languages"),
        key=f"{PAGE}.lan_ds",
        default=st.session_state.get(f"{PAGE}.lan_ds", []),
    )
    st.multiselect(
        "**LicenseToUse**",
        dao.get_all("Datasets", "licenseToUse"),
        key=f"{PAGE}.lic",
        default=st.session_state.get(f"{PAGE}.lic", []),
    )

with col_15:
    st.html(
        """
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        """
    )

# Initialise dataset filters
st.session_state[f"{PAGE}.filters_ds"] = {}
st.session_state[f"{PAGE}.size_filter_active"] = False

# Handle dataset size filter on string values (e.g. '194k', '2M')
if st.session_state[f"{PAGE}.type_filter"] == "Row count":
    min_rows = st.session_state[f"{PAGE}.min_size_rows"]
    max_rows = (
        st.session_state[f"{PAGE}.max_size_rows"]
        if st.session_state[f"{PAGE}.max_size_rows"]
        else 1e9
    )
    st.session_state[f"{PAGE}.size_filter_active"] = True
    st.session_state[f"{PAGE}.min_rows"] = min_rows
    st.session_state[f"{PAGE}.max_rows"] = max_rows

# Fine-tuning flag
if st.session_state[f"{PAGE}.fine_tuning"] != "No filter":
    st.session_state[f"{PAGE}.filters_ds"]["fineTuning"] = st.session_state[f"{PAGE}.fine_tuning"] == "True"

# Domain filter - datasets have domain as arrays, so we need to match arrays that contain
# any of our requested domains. For simple arrays, use $in directly.
if st.session_state[f"{PAGE}.domain"]:
    # For simple array fields, MongoDB's $in operator matches if any array element is in our list
    st.session_state[f"{PAGE}.filters_ds"]["domain"] = {
        "$in": st.session_state[f"{PAGE}.domain"]
    }

# License filter
if st.session_state[f"{PAGE}.lic"]:
    st.session_state[f"{PAGE}.filters_ds"]["licenseToUse"] = {
        "$all": st.session_state[f"{PAGE}.lic"]
    }

# Language filter
if st.session_state[f"{PAGE}.lan_ds"]:
    st.session_state[f"{PAGE}.filters_ds"]["languages"] = {
        "$all": st.session_state[f"{PAGE}.lan_ds"]
    }

# -----------------------------------------------------------------------------
# FINAL SECTION FOR QUERYING AND DISPLAY
# -----------------------------------------------------------------------------
st.markdown("---")
# Choose which fields to display from models and datasets
st.multiselect(
    "**Select the results of the query for LLM**",
    dao.get_attributes(MODELS),
    st.session_state.get(f"{PAGE}.project_llm_multiselect", ["name", "version", "numberOfParameters"]),
    key=f"{PAGE}.project_llm_multiselect",
)

st.multiselect(
    "**Select the results of the query for Dataset**",
    dao.get_attributes(DATASETS),
    st.session_state.get(f"{PAGE}.project_ds_multiselect", ["name", "uri", "domain"]),
    key=f"{PAGE}.project_ds_multiselect",
)

with st.expander("**📊 Ranking Options**", expanded=False):
    st.radio(
        "**Rank by**",
        ["No ranking", "Model Parameters", "Model Carbon Emissions", "Dataset Size"],
        index=0,
        key=f"{PAGE}.rank_by"
    )
    if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
        st.radio(
            "**Sort order**",
            ["Ascending (Low to High)", "Descending (High to Low)"],
            index=1,
            key=f"{PAGE}.sort_order"
        )

# Button to trigger the query
l, l1, c, r1, r = st.columns(5)
with c:
    query = st.button("Get results")

if query:
    # -------------------------------------------------------------------------
    # Build projection lists, ensuring fields needed for manual filtering are
    # included when the corresponding filters are active. Without these
    # additional fields, later numeric comparisons would fail because the
    # values would not be present in the results.
    llm_project_fields = st.session_state[f"{PAGE}.project_llm_multiselect"].copy()
    
    # Always include _id for joining with edges
    if "_id" not in llm_project_fields:
        llm_project_fields.append("_id")
    
    if (
        st.session_state.get(f"{PAGE}.param_filter_active", False)
        and "numberOfParameters" not in llm_project_fields
    ):
        llm_project_fields.append("numberOfParameters")
    if (
        st.session_state.get(f"{PAGE}.carbon_filter_active", False)
        and "carbon_emissions_tco2e" not in llm_project_fields
    ):
        llm_project_fields.append("carbon_emissions_tco2e")

    # Add ranking fields to project if ranking is active
    if st.session_state[f"{PAGE}.rank_by"] == "Model Parameters" and "numberOfParameters" not in llm_project_fields:
        llm_project_fields.append("numberOfParameters")
    elif st.session_state[f"{PAGE}.rank_by"] == "Model Carbon Emissions" and "carbon_emissions_tco2e" not in llm_project_fields:
        llm_project_fields.append("carbon_emissions_tco2e")

    dataset_project_fields = st.session_state[f"{PAGE}.project_ds_multiselect"].copy()
    
    # Always include _id for joining with edges
    if "_id" not in dataset_project_fields:
        dataset_project_fields.append("_id")
        
    if (
        st.session_state.get(f"{PAGE}.size_filter_active", False)
        and "size" not in dataset_project_fields
    ):
        dataset_project_fields.append("size")

    # Add ranking fields to project if ranking is active
    if st.session_state[f"{PAGE}.rank_by"] == "Dataset Size" and "size" not in dataset_project_fields:
        dataset_project_fields.append("size")

    # -------------------------------------------------------------------------
    # Query models collection with selected projection and filters
    models_query = create_query_structure(
        collection=MODELS,
        project=llm_project_fields,
        filters=st.session_state[f"{PAGE}.filters_llm"],
    )
    models_result = dao.query([models_query])

    # Manual post‑processing for number of parameters
    if st.session_state.get(f"{PAGE}.param_filter_active", False):
        def convert_params_to_numeric(param_str: str) -> float:
            """Convert parameter strings like '7B' or '176M' to numeric (billions)"""
            if not param_str:
                return 0.0
            param_str = str(param_str).upper()
            try:
                if param_str.endswith("B"):
                    return float(param_str[:-1])
                if param_str.endswith("M"):
                    return float(param_str[:-1]) / 1000.0
                return float(param_str)
            except Exception:
                return 0.0

        min_params = st.session_state[f"{PAGE}.min_params"]
        max_params = st.session_state[f"{PAGE}.max_params"]
        filtered_models = []
        for item in models_result:
            param_value = None
            # Expect model fields under the "Models" key
            if "Models" in item and "numberOfParameters" in item["Models"]:
                param_value = item["Models"]["numberOfParameters"]
            if param_value is not None:
                numeric_params = convert_params_to_numeric(param_value)
                if min_params <= numeric_params <= max_params:
                    filtered_models.append(item)
            elif min_params == 0:
                # if no param specified and minimum is zero, include
                filtered_models.append(item)
        models_result = filtered_models

    # Manual post‑processing for carbon emissions
    if st.session_state.get(f"{PAGE}.carbon_filter_active", False):
        min_carbon = st.session_state[f"{PAGE}.min_carbon_val"]
        max_carbon = st.session_state[f"{PAGE}.max_carbon_val"]
        filtered_models = []
        for item in models_result:
            carbon_value = None
            if "Models" in item and "carbon_emissions_tco2e" in item["Models"]:
                carbon_value = item["Models"]["carbon_emissions_tco2e"]
            if carbon_value is not None:
                try:
                    numeric_carbon = float(carbon_value)
                    if min_carbon <= numeric_carbon <= max_carbon:
                        filtered_models.append(item)
                except Exception:
                    # skip items where conversion fails
                    pass
            elif min_carbon == 0:
                filtered_models.append(item)
        models_result = filtered_models

    # -------------------------------------------------------------------------
    # Query datasets collection with selected projection and filters
    datasets_query = create_query_structure(
        collection=DATASETS,
        project=dataset_project_fields,
        filters=st.session_state[f"{PAGE}.filters_ds"],
    )
    datasets_result = dao.query([datasets_query])

    # Manual post‑processing for dataset size (string to numeric)
    if st.session_state.get(f"{PAGE}.size_filter_active", False):
        def convert_size_to_numeric(size_str: str) -> float:
            """Convert size strings like '194k' or '2M' to numeric rows."""
            if not size_str or size_str == "n/a":
                return 0.0
            size_str = str(size_str).lower()
            try:
                if size_str.endswith("k"):
                    return float(size_str[:-1]) * 1_000
                if size_str.endswith("m"):
                    return float(size_str[:-1]) * 1_000_000
                return float(size_str)
            except Exception:
                return 0.0

        min_rows = st.session_state[f"{PAGE}.min_rows"]
        max_rows = st.session_state[f"{PAGE}.max_rows"]
        filtered_datasets = []
        for item in datasets_result:
            size_value = None
            if "Datasets" in item and "size" in item["Datasets"]:
                size_value = item["Datasets"]["size"]
            if size_value is not None:
                numeric_size = convert_size_to_numeric(size_value)
                if min_rows <= numeric_size <= max_rows:
                    filtered_datasets.append(item)
            elif min_rows == 0:
                filtered_datasets.append(item)
        datasets_result = filtered_datasets

    # -------------------------------------------------------------------------
    # Retrieve all trained_on and fine_tuned_on edges from the Edges collection. 
    # These records describe which model was trained/fine-tuned on which dataset.
    
    edges_query = create_query_structure(
        collection="Edges",
        project=["from", "to", "relation_type"],
        filters={"$or": [
            {"relation_type": "trained_on"},
            {"relation_type": "fine_tuned_on"}
        ]},
    )
    edges_result = dao.query([edges_query])

    # -------------------------------------------------------------------------
    # Combine models and datasets according to the edges. We need to group by model
    # and check if the union of all associated dataset domains contains ALL requested domains.
    # We strip the ``model:`` and ``dataset:`` prefixes when comparing IDs because the
    # underlying entries in the Models and Datasets collections do not include
    # these prefixes in their ``_id`` fields.
    
    # First, create a mapping of model_id -> list of associated datasets
    model_datasets = {}
    for edge in edges_result:
        if "Edges" not in edge:
            continue
        edge_data = edge["Edges"]
        model_id = edge_data.get("from", "").replace("model:", "")
        dataset_id = edge_data.get("to", "").replace("dataset:", "")
        
        # find matching model
        matching_model = None
        for model in models_result:
            if "Models" in model:
                current_id = model["Models"].get("_id", "").replace("model:", "")
                if current_id == model_id:
                    matching_model = model
                    break

        # find matching dataset
        matching_dataset = None
        for dataset in datasets_result:
            if "Datasets" in dataset:
                current_id = dataset["Datasets"].get("_id", "").replace("dataset:", "")
                if current_id == dataset_id:
                    matching_dataset = dataset
                    break

        # if both sides match, group by model
        if matching_model and matching_dataset:
            if model_id not in model_datasets:
                model_datasets[model_id] = {
                    'model': matching_model,
                    'datasets': []
                }
            model_datasets[model_id]['datasets'].append(matching_dataset)
    
    # Now check which models have datasets covering ALL requested domains
    requested_domains = set(st.session_state.get(f"{PAGE}.domain", []))
    joined_results = []
    
    for model_id, model_data in model_datasets.items():
        # Collect all domains from this model's datasets  
        model_domains = set()
        for dataset in model_data['datasets']:
            if "Datasets" in dataset and "domain" in dataset["Datasets"]:
                dataset_domains = dataset["Datasets"]["domain"]
                # Handle both single domain and list of domains
                if isinstance(dataset_domains, list):
                    model_domains.update(dataset_domains)
                else:
                    model_domains.add(dataset_domains)
        
        # Check if this model's datasets cover ALL requested domains
        if requested_domains.issubset(model_domains):
            # Create combined results for this model with all its relevant datasets
            model_info = model_data['model']
            for dataset in model_data['datasets']:
                joined_result = {**model_info, **dataset}
                joined_results.append(joined_result)
    
    # -------------------------------------------------------------------------
    # Display the joined results in a dataframe. If no matching edges exist,
    # provide a user‑friendly message instead.
    if joined_results:
        # Apply ranking if selected
        if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
            def convert_params_to_numeric(param_str):
                """Convert parameter strings like '7B', '176B' to numeric values in billions"""
                if not param_str:
                    return None
                param_str = str(param_str).upper()
                if param_str.endswith('B'):
                    try:
                        return float(param_str[:-1])
                    except ValueError:
                        return None
                elif param_str.endswith('M'):
                    try:
                        return float(param_str[:-1]) / 1000
                    except ValueError:
                        return None
                else:
                    try:
                        return float(param_str) / 1000000000
                    except ValueError:
                        return None
            
            def convert_size_to_numeric(size_str):
                """Convert size strings like '273k', '2M' to numeric values"""
                if not size_str or size_str == "n/a":
                    return None
                size_str = str(size_str).upper()
                if size_str.endswith('K'):
                    try:
                        return float(size_str[:-1]) * 1000
                    except ValueError:
                        return None
                elif size_str.endswith('M'):
                    try:
                        return float(size_str[:-1]) * 1000000
                    except ValueError:
                        return None
                else:
                    try:
                        return float(size_str)
                    except ValueError:
                        return None
            
            def has_valid_ranking_value(item):
                """Check if item has a valid (non-null) value for the selected ranking field"""
                if st.session_state[f"{PAGE}.rank_by"] == "Model Parameters":
                    # Access the field from the Models section
                    if "Models" in item and "numberOfParameters" in item["Models"]:
                        param_value = item["Models"]["numberOfParameters"]
                        return convert_params_to_numeric(param_value) is not None
                    return False
                elif st.session_state[f"{PAGE}.rank_by"] == "Model Carbon Emissions":
                    if "Models" in item and "carbon_emissions_tco2e" in item["Models"]:
                        try:
                            value = item["Models"]["carbon_emissions_tco2e"]
                            return value is not None and float(value) is not None
                        except (ValueError, TypeError):
                            return False
                    return False
                elif st.session_state[f"{PAGE}.rank_by"] == "Dataset Size":
                    # Access the field from the Datasets section
                    if "Datasets" in item and "size" in item["Datasets"]:
                        size_value = item["Datasets"]["size"]
                        return convert_size_to_numeric(size_value) is not None
                    return False
                return True
            
            def get_sort_key(item):
                if st.session_state[f"{PAGE}.rank_by"] == "Model Parameters":
                    if "Models" in item and "numberOfParameters" in item["Models"]:
                        param_value = item["Models"]["numberOfParameters"]
                        return convert_params_to_numeric(param_value) or 0
                    return 0
                elif st.session_state[f"{PAGE}.rank_by"] == "Model Carbon Emissions":
                    if "Models" in item and "carbon_emissions_tco2e" in item["Models"]:
                        try:
                            return float(item["Models"]["carbon_emissions_tco2e"])
                        except (ValueError, TypeError):
                            return 0
                    return 0
                elif st.session_state[f"{PAGE}.rank_by"] == "Dataset Size":
                    if "Datasets" in item and "size" in item["Datasets"]:
                        size_value = item["Datasets"]["size"]
                        return convert_size_to_numeric(size_value) or 0
                    return 0
                return 0
            
            # Filter out items with null/missing ranking values
            joined_results = [item for item in joined_results if has_valid_ranking_value(item)]
            
            # Sort the remaining items
            reverse_order = st.session_state[f"{PAGE}.sort_order"] == "Descending (High to Low)"
            joined_results = sorted(joined_results, key=get_sort_key, reverse=reverse_order)
        
        df = pd.DataFrame(reworked_query_output(joined_results))
        st.dataframe(df)
    else:
        st.write(
            "No training relationships found matching the specified filters."
        )
