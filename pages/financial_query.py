import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

# This Streamlit page provides a pre-configured query showing open-source models
# with less than 8B parameters suited for Financial Document Analysis tasks.

PAGE = "Query 2 - Finance"
DOWNSTREAM_TASKS = "Downstream Tasks"
MODELS = "Models"
DB_NAME = "ChatIMPACT"

# Initialise data access object
dao = Dao(DB_NAME)

# Initialize session state with predefined filters FIRST - before any UI components
if f"{PAGE}.initialized" not in st.session_state:
    # Task filters
    st.session_state[f"{PAGE}.name_dt"] = ["Financial Document Analysis"]
    
    # Model filters
    st.session_state[f"{PAGE}.open_source"] = "True"
    st.session_state[f"{PAGE}.instruction_tuned"] = "No filter"
    st.session_state[f"{PAGE}.num_param_filter"] = "Number of Parameters (B)"
    st.session_state[f"{PAGE}.min_num_param"] = 0.0
    st.session_state[f"{PAGE}.max_num_param"] = 8.0
    st.session_state[f"{PAGE}.carbon_filter"] = "No filters"
    st.session_state[f"{PAGE}.lan_llm"] = []
    st.session_state[f"{PAGE}.license"] = []
    
    # Display options
    st.session_state[f"{PAGE}.project_llm_multiselect"] = ["name", "version", "numberOfParameters"]
    st.session_state[f"{PAGE}.project_dt_multiselect"] = ["name", "description"]
    
    # Ranking options
    st.session_state[f"{PAGE}.rank_by"] = "No ranking"
    st.session_state[f"{PAGE}.sort_order"] = "Descending (High to Low)"
    
    st.session_state[f"{PAGE}.initialized"] = True

# Page navigation and title
st.page_link("gui.py", label="Homepage", icon="🏠")
title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"
st.html(title_alignment)

# Add the query image
st.markdown('<img src="./app/static/2.png" alt="Query 2" width="1000" height="200">', unsafe_allow_html=True)

st.markdown("""
**Pre-configured Query:** *"Find the open-source models specialized in Financial Document Analysis with less than 8B parameters."*

This query considers the **SuitedFor** relationship between the **Model** and **Task** entities with the following pre-configured filters:
            
- **Model filters:** OpenSource=True, NumberOfParameters < 8B  
- **Task filters:** SubTask = Financial Document Analysis  
            
The filters are already applied in the sections below.
""")

# -----------------------------------------------------------------------------
# SECTION FOR DOWNSTREAM TASK FILTERS (PRE-CONFIGURED)
# -----------------------------------------------------------------------------
st.markdown("---")
st.html(f"<h3 style='text-align: center;'>{DOWNSTREAM_TASKS} filters</h3>")

col_dt1, col_dt2 = st.columns(2)
with col_dt1:
    st.multiselect(
        "**Downstream Task**",
        dao.get_all("Downstream Tasks", "name"),
        key=f"{PAGE}.name_dt",
        default=st.session_state.get(f"{PAGE}.name_dt", ["Financial Document Analysis"]),
        help="Select specific downstream tasks to find models suited for them. Leave empty to show all task-model relationships."
    )

with col_dt2:
    # Show available task names for reference
    all_task_names = dao.get_all("Downstream Tasks", "name")
    st.info(f"Available tasks: {', '.join(all_task_names)}")

# Initialize downstream task filters
st.session_state[f"{PAGE}.filters_dt"] = {}

# Add task name filter if selected
if st.session_state[f"{PAGE}.name_dt"]:
    st.session_state[f"{PAGE}.filters_dt"]["name"] = {
        "$in": st.session_state[f"{PAGE}.name_dt"]
    }

# -----------------------------------------------------------------------------
# SECTION FOR LARGE LANGUAGE MODEL FILTERS (PRE-CONFIGURED)
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
        index=1,  # Pre-select "Number of Parameters (B)"
        key=f"{PAGE}.num_param_filter"
    )
    if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
        st.number_input(
            "**Minimum number of parameters (B)**", 
            min_value=0.0, 
            value=st.session_state.get(f"{PAGE}.min_num_param", 0.0), 
            step=0.1,
            key=f"{PAGE}.min_num_param"
        )
        st.number_input(
            "**Maximum number of parameters (B)**", 
            min_value=0.0, 
            value=st.session_state.get(f"{PAGE}.max_num_param", 8.0), 
            step=0.1,
            key=f"{PAGE}.max_num_param"
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
    st.radio(
        "**Open Source**", 
        ["No filter", "True", "False"], 
        index=1,  # Pre-select "True"
        key=f"{PAGE}.open_source"
    )
    st.radio(
        "**Instruction Tuned**", 
        ["No filter", "True", "False"], 
        index=0,  # Pre-select "No filter"
        key=f"{PAGE}.instruction_tuned"
    )
    st.radio(
        "***Filter on Carbon Emissions***",
        ["No filters", "Carbon Emissions (tCO2e)"],
        index=0,  # Pre-select "No filters"
        key=f"{PAGE}.carbon_filter"
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
        default=[],  # Pre-configured as empty
        key=f"{PAGE}.lan_llm"
    )
    st.multiselect(
        "**License to Use**",
        dao.get_all("Models", "license_to_use"),
        default=[],  # Pre-configured as empty
        key=f"{PAGE}.license"
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
    min_params = st.session_state[f"{PAGE}.min_num_param"]
    max_params = st.session_state[f"{PAGE}.max_num_param"]
    st.session_state[f"{PAGE}.param_filter_active"] = True
    st.session_state[f"{PAGE}.min_params"] = min_params
    st.session_state[f"{PAGE}.max_params"] = max_params

# Handle carbon emissions filter
if st.session_state[f"{PAGE}.carbon_filter"] == "Carbon Emissions (tCO2e)":
    min_carbon = st.session_state[f"{PAGE}.min_carbon"]
    max_carbon = st.session_state[f"{PAGE}.max_carbon"]
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
# FINAL SECTION FOR QUERYING AND DISPLAY
# -----------------------------------------------------------------------------
st.markdown("---")
# Choose which fields to display from models and tasks
st.multiselect(
    "**Select the results of the query for LLM**",
    dao.get_attributes(MODELS),
    default=st.session_state.get(f"{PAGE}.project_llm_multiselect", ["name", "version", "numberOfParameters"]),
    key=f"{PAGE}.project_llm_multiselect"
)

st.multiselect(
    "**Select the results of the query for Downstream Task**",
    dao.get_attributes(DOWNSTREAM_TASKS),
    default=st.session_state.get(f"{PAGE}.project_dt_multiselect", ["name", "description"]),
    key=f"{PAGE}.project_dt_multiselect"
)

with st.expander("**📊 Ranking Options**", expanded=False):
    st.radio(
        "**Rank by**",
        ["No ranking", "Number of Parameters", "Carbon Emissions"],
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
    if st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Number of Parameters" and "numberOfParameters" not in llm_project_fields:
        llm_project_fields.append("numberOfParameters")
    elif st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Carbon Emissions" and "carbon_emissions_tco2e" not in llm_project_fields:
        llm_project_fields.append("carbon_emissions_tco2e")

    task_project_fields = st.session_state[f"{PAGE}.project_dt_multiselect"].copy()
    
    # Always include _id for joining with edges
    if "_id" not in task_project_fields:
        task_project_fields.append("_id")

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
    # Retrieve all suited_for edges from the Edges collection first
    # These records describe which model is suited for which task.
    
    edges_query = create_query_structure(
        collection="Edges",
        project=["from", "to", "relation_type"],
        filters={"relation_type": "suited_for"},
    )
    edges_result = dao.query([edges_query])

    # -------------------------------------------------------------------------
    # If task names are selected, filter edges to only those targeting selected tasks
    # We need to map task display names to task IDs first
    filtered_edges = edges_result
    if st.session_state[f"{PAGE}.name_dt"]:
        # Get all tasks to map names to IDs
        all_tasks_query = create_query_structure(
            collection=DOWNSTREAM_TASKS,
            project=["_id", "name"],
            filters={},
        )
        all_tasks_result = dao.query([all_tasks_query])
        
        # Create mapping from display name to task ID
        name_to_id = {}
        for task in all_tasks_result:
            if "Downstream Tasks" in task:
                task_data = task["Downstream Tasks"]
                name_to_id[task_data.get("name", "")] = task_data.get("_id", "")
        
        # Get task IDs for selected names
        selected_task_ids = []
        for selected_name in st.session_state[f"{PAGE}.name_dt"]:
            if selected_name in name_to_id:
                selected_task_ids.append(name_to_id[selected_name])
        
        # Filter edges to only those targeting selected tasks
        filtered_edges = []
        for edge in edges_result:
            if "Edges" in edge:
                edge_data = edge["Edges"]
                target_task = edge_data.get("to", "")
                if target_task in selected_task_ids:
                    filtered_edges.append(edge)

    # -------------------------------------------------------------------------
    # Get all unique task IDs from the filtered edges
    task_ids_needed = set()
    for edge in filtered_edges:
        if "Edges" in edge:
            task_ids_needed.add(edge["Edges"].get("to", ""))
    
    # Query tasks collection for only the tasks we need
    if task_ids_needed:
        all_tasks_query = create_query_structure(
            collection=DOWNSTREAM_TASKS,
            project=task_project_fields,
            filters={},
        )
        all_tasks_result = dao.query([all_tasks_query])
        
        # Filter manually to only the tasks we need
        tasks_result = []
        for task in all_tasks_result:
            if "Downstream Tasks" in task:
                task_id = task["Downstream Tasks"].get("_id", "")
                if task_id in task_ids_needed:
                    tasks_result.append(task)
    else:
        tasks_result = []

    # -------------------------------------------------------------------------
    # Combine models and tasks according to the edges. Only those pairs
    # passing their respective filters will be displayed. We strip the
    # ``model:`` and ``task:`` prefixes when comparing IDs because the
    # underlying entries in the Models and Downstream Tasks collections do not include
    # these prefixes in their ``_id`` fields.
    joined_results = []
    for edge in filtered_edges:
        if "Edges" not in edge:
            continue
        edge_data = edge["Edges"]
        model_id = edge_data.get("from", "").replace("model:", "")
        task_id = edge_data.get("to", "").replace("task:", "")
        
        # find matching model
        matching_model = None
        for model in models_result:
            if "Models" in model:
                current_id = model["Models"].get("_id", "").replace("model:", "")
                if current_id == model_id:
                    matching_model = model
                    break

        # find matching task
        matching_task = None
        for task in tasks_result:
            if "Downstream Tasks" in task:
                current_id = task["Downstream Tasks"].get("_id", "").replace("task:", "")
                if current_id == task_id:
                    matching_task = task
                    break

        # if both sides match, combine
        if matching_model and matching_task:
            # merge dictionaries – keys from matching_task will overwrite duplicates
            joined_result = {**matching_model, **matching_task}
            joined_results.append(joined_result)

    # -------------------------------------------------------------------------
    # Display the joined results in a dataframe. If no matching edges exist,
    # provide a user‑friendly message instead.
    if joined_results:
        # Apply ranking if selected
        if st.session_state.get(f"{PAGE}.rank_by", "No ranking") != "No ranking":
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
            
            def has_valid_ranking_value(item):
                """Check if item has a valid (non-null) value for the selected ranking field"""
                if st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Number of Parameters":
                    if "Models" in item and "numberOfParameters" in item["Models"]:
                        return convert_params_to_numeric(item["Models"]["numberOfParameters"]) is not None
                    return False
                elif st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Carbon Emissions":
                    if "Models" in item and "carbon_emissions_tco2e" in item["Models"]:
                        try:
                            value = item["Models"]["carbon_emissions_tco2e"]
                            return value is not None and float(value) is not None
                        except (ValueError, TypeError):
                            return False
                    return False
                return True
            
            def get_sort_key(item):
                if st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Number of Parameters":
                    if "Models" in item and "numberOfParameters" in item["Models"]:
                        return convert_params_to_numeric(item["Models"]["numberOfParameters"]) or 0
                    return 0
                elif st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Carbon Emissions":
                    if "Models" in item and "carbon_emissions_tco2e" in item["Models"]:
                        try:
                            return float(item["Models"]["carbon_emissions_tco2e"])
                        except (ValueError, TypeError):
                            return 0
                    return 0
                return 0
            
            # Filter out items with null/missing ranking values
            joined_results = [item for item in joined_results if has_valid_ranking_value(item)]
            
            # Sort the remaining items
            reverse_order = st.session_state.get(f"{PAGE}.sort_order", "Descending (High to Low)") == "Descending (High to Low)"
            joined_results = sorted(joined_results, key=get_sort_key, reverse=reverse_order)
        
        st.success(f"Found {len(joined_results)} model-task relationships matching your filters.")
        df = pd.DataFrame(reworked_query_output(joined_results))
        st.dataframe(df)
        
        # Show summary of what was found
        model_names = set()
        task_names = set()
        for result in joined_results:
            if "Models" in result:
                model_names.add(result["Models"].get("name", "Unknown"))
            if "Downstream Tasks" in result:
                task_names.add(result["Downstream Tasks"].get("name", "Unknown"))
        
        st.info(f"**Found Models:** {', '.join(sorted(model_names))}")
        st.info(f"**Found Tasks:** {', '.join(sorted(task_names))}")
    else:
        st.warning("No 'suited for' relationships found matching the specified filters.")
        st.info("This means there are no open-source models with less than 8B parameters suited for Financial Document Analysis in the current database.")
