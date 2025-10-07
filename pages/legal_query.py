import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

# This Streamlit page provides a pre-configured query showing datasets to train models
# for text summarization in legal domains, with docs in English, Italian, Spanish, German, and French.

PAGE = "Query 3 - Legal"
DOWNSTREAM_TASKS = "Downstream Tasks"
DATASETS = "Datasets"
DB_NAME = "ChatIMPACT"

# Initialise data access object
dao = Dao(DB_NAME)

# Initialize session state with predefined filters FIRST - before any UI components
if f"{PAGE}.initialized" not in st.session_state:
    # Task filters
    st.session_state[f"{PAGE}.name_dt"] = ["Text Summarization"]
    
    # Dataset filters
    st.session_state[f"{PAGE}.type_filter"] = "No filters"
    st.session_state[f"{PAGE}.fine_tuning"] = "No filter"
    st.session_state[f"{PAGE}.domain"] = ["Law"]
    st.session_state[f"{PAGE}.lan_ds"] = ["English", "Italian", "Spanish", "German", "French"]
    st.session_state[f"{PAGE}.lic"] = []
    
    # Display options
    st.session_state[f"{PAGE}.project_dt_multiselect"] = ["name", "description"]
    st.session_state[f"{PAGE}.project_ds_multiselect"] = ["name", "uri", "domain"]
    
    # Ranking options
    st.session_state[f"{PAGE}.rank_by"] = "No ranking"
    st.session_state[f"{PAGE}.sort_order"] = "Descending (High to Low)"
    
    st.session_state[f"{PAGE}.initialized"] = True

# Page navigation and title
st.page_link("gui.py", label="Homepage", icon="🏠")
title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"
st.html(title_alignment)

# Add the query image
st.markdown('<img src="./app/static/3.png" alt="Query 3" width="1000" height="200">', unsafe_allow_html=True)

st.markdown("""
**Pre-configured Query:** *"Find datasets to train models for text summarization in legal domains, with docs in English, Italian, Spanish, German, and French."*

This query uses the **enabled_by** relationship between **Dataset** and **Task** entities with the following pre-configured filters:
            
- **Task filters:** Downstream Task = Text Summarization  
- **Dataset filters:** Domain=Law, Language ∈ {English, Italian, Spanish, German, French}  
            
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
        default=st.session_state.get(f"{PAGE}.name_dt", ["Text Summarization"]),
        help="Select specific downstream tasks to find datasets that enable them. Leave empty to show all task-dataset relationships."
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
# SECTION FOR DATASET FILTERS (PRE-CONFIGURED)
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
        index=0,  # Pre-select "No filters"
        key=f"{PAGE}.type_filter"
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
    st.radio(
        "**Fine-Tuning Dataset**", 
        ["No filter", "True", "False"], 
        index=0,  # Pre-select "No filter"
        key=f"{PAGE}.fine_tuning"
    )
    # domain selection
    st.multiselect(
        "**Domain**",
        dao.get_all("Datasets", "domain"),
        default=st.session_state.get(f"{PAGE}.domain", ["Law"]),  # Pre-select "Law"
        key=f"{PAGE}.domain"
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
        default=st.session_state.get(f"{PAGE}.lan_ds", ["English", "Italian", "Spanish", "German", "French"]),  # Pre-select multiple languages
        key=f"{PAGE}.lan_ds"
    )
    st.multiselect(
        "**LicenseToUse**",
        dao.get_all("Datasets", "licenseToUse"),
        default=[],  # Pre-configured as empty
        key=f"{PAGE}.lic"
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
    min_rows = st.session_state.get(f"{PAGE}.min_size_rows", 0)
    max_rows = st.session_state.get(f"{PAGE}.max_size_rows", 1e9)
    st.session_state[f"{PAGE}.size_filter_active"] = True
    st.session_state[f"{PAGE}.min_rows"] = min_rows
    st.session_state[f"{PAGE}.max_rows"] = max_rows

# Fine-tuning flag
if st.session_state[f"{PAGE}.fine_tuning"] != "No filter":
    st.session_state[f"{PAGE}.filters_ds"]["fineTuning"] = st.session_state[f"{PAGE}.fine_tuning"] == "True"

# Domain filter
if st.session_state[f"{PAGE}.domain"]:
    st.session_state[f"{PAGE}.filters_ds"]["domain"] = {
        "$all": st.session_state[f"{PAGE}.domain"]
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
# Choose which fields to display from tasks and datasets
st.multiselect(
    "**Select the results of the query for Downstream Task**",
    dao.get_attributes(DOWNSTREAM_TASKS),
    default=st.session_state.get(f"{PAGE}.project_dt_multiselect", ["name", "description"]),
    key=f"{PAGE}.project_dt_multiselect"
)

st.multiselect(
    "**Select the results of the query for Dataset**",
    dao.get_attributes(DATASETS),
    default=st.session_state.get(f"{PAGE}.project_ds_multiselect", ["name", "uri", "domain"]),
    key=f"{PAGE}.project_ds_multiselect"
)

with st.expander("**📊 Ranking Options**", expanded=False):
    st.radio(
        "**Rank by**",
        ["No ranking", "Dataset Size"],
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
    task_project_fields = st.session_state[f"{PAGE}.project_dt_multiselect"].copy()
    
    # Always include _id for joining with edges
    if "_id" not in task_project_fields:
        task_project_fields.append("_id")

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
    if st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Dataset Size" and "size" not in dataset_project_fields:
        dataset_project_fields.append("size")

    # -------------------------------------------------------------------------
    # Retrieve all enabled_by edges from the Edges collection first
    # These records describe which task is enabled by which dataset.
    
    edges_query = create_query_structure(
        collection="Edges",
        project=["from", "to", "relation_type"],
        filters={"relation_type": "enabled_by"},
    )
    edges_result = dao.query([edges_query])

    # -------------------------------------------------------------------------
    # If task names are selected, filter edges to only those from selected tasks
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
        
        # Filter edges to only those from selected tasks
        filtered_edges = []
        for edge in edges_result:
            if "Edges" in edge:
                edge_data = edge["Edges"]
                source_task = edge_data.get("from", "")
                if source_task in selected_task_ids:
                    filtered_edges.append(edge)

    # -------------------------------------------------------------------------
    # Get all unique task and dataset IDs from the filtered edges
    task_ids_needed = set()
    dataset_ids_needed = set()
    for edge in filtered_edges:
        if "Edges" in edge:
            task_ids_needed.add(edge["Edges"].get("from", ""))
            dataset_ids_needed.add(edge["Edges"].get("to", ""))
    
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
    # Combine tasks and datasets according to the edges. Only those pairs
    # passing their respective filters will be displayed. We strip the
    # ``task:`` and ``dataset:`` prefixes when comparing IDs because the
    # underlying entries in the Downstream Tasks and Datasets collections do not include
    # these prefixes in their ``_id`` fields.
    joined_results = []
    for edge in filtered_edges:
        if "Edges" not in edge:
            continue
        edge_data = edge["Edges"]
        task_id = edge_data.get("from", "").replace("task:", "")
        dataset_id = edge_data.get("to", "").replace("dataset:", "")
        
        # find matching task
        matching_task = None
        for task in tasks_result:
            if "Downstream Tasks" in task:
                current_id = task["Downstream Tasks"].get("_id", "").replace("task:", "")
                if current_id == task_id:
                    matching_task = task
                    break

        # find matching dataset
        matching_dataset = None
        for dataset in datasets_result:
            if "Datasets" in dataset:
                current_id = dataset["Datasets"].get("_id", "").replace("dataset:", "")
                if current_id == dataset_id:
                    matching_dataset = dataset
                    break

        # if both sides match, combine
        if matching_task and matching_dataset:
            # merge dictionaries – keys from matching_dataset will overwrite duplicates
            joined_result = {**matching_task, **matching_dataset}
            joined_results.append(joined_result)

    # -------------------------------------------------------------------------
    # Display the joined results in a dataframe. If no matching edges exist,
    # provide a user‑friendly message instead.
    if joined_results:
        # Apply ranking if selected
        if st.session_state.get(f"{PAGE}.rank_by", "No ranking") != "No ranking":
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
                if st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Dataset Size":
                    if "Datasets" in item and "size" in item["Datasets"]:
                        return convert_size_to_numeric(item["Datasets"]["size"]) is not None
                    return False
                return True
            
            def get_sort_key(item):
                if st.session_state.get(f"{PAGE}.rank_by", "No ranking") == "Dataset Size":
                    if "Datasets" in item and "size" in item["Datasets"]:
                        return convert_size_to_numeric(item["Datasets"]["size"]) or 0
                    return 0
                return 0
            
            # Filter out items with null/missing ranking values
            joined_results = [item for item in joined_results if has_valid_ranking_value(item)]
            
            # Sort the remaining items
            reverse_order = st.session_state.get(f"{PAGE}.sort_order", "Descending (High to Low)") == "Descending (High to Low)"
            joined_results = sorted(joined_results, key=get_sort_key, reverse=reverse_order)
        
        st.success(f"Found {len(joined_results)} task-dataset relationships matching your filters.")
        df = pd.DataFrame(reworked_query_output(joined_results))
        st.dataframe(df)
        
        # Show summary of what was found
        task_names = set()
        dataset_names = set()
        for result in joined_results:
            if "Downstream Tasks" in result:
                task_names.add(result["Downstream Tasks"].get("name", "Unknown"))
            if "Datasets" in result:
                dataset_names.add(result["Datasets"].get("name", "Unknown"))
        
        st.info(f"**Found Tasks:** {', '.join(sorted(task_names))}")
        st.info(f"**Found Datasets:** {', '.join(sorted(dataset_names))}")
    else:
        st.warning("No 'enabled by' relationships found matching the specified filters.")
        st.info("This means there are no datasets for text summarization in legal domains with the specified languages in the current database.")
