import streamlit as st
import pandas as pd
import json
import os
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Query 6 - Software Development"
DOWNSTREAM_TASKS = "Downstream Tasks"
MODELS = "Models"
METRICS = "Metrics"
DB_NAME = "ChatIMPACT"

# Initialise data access object
dao = Dao(DB_NAME)

# Initialize session state with predefined filters FIRST - before any UI components
if f"{PAGE}.initialized" not in st.session_state:
    # Task filters - pre-configured for Code Generation
    st.session_state[f"{PAGE}.assesses_downstream_task"] = ["Code Generation"]
    
    # Metric filters - pre-configured for Tabby (suitable for code generation)
    st.session_state[f"{PAGE}.contextFree"] = "No filter"
    st.session_state[f"{PAGE}.trained"] = "No filter"
    st.session_state[f"{PAGE}.featureBased"] = "No filter"
    st.session_state[f"{PAGE}.granularity"] = []
    st.session_state[f"{PAGE}.feat"] = []
    st.session_state[f"{PAGE}.metric_name"] = ["Tabby"]
    
    # Model filters - pre-configured for instruction-tuned models < 8B
    st.session_state[f"{PAGE}.num_param_filter"] = "Number of Parameters (B)"
    st.session_state[f"{PAGE}.min_num_param"] = 0.0
    st.session_state[f"{PAGE}.max_num_param"] = 8.0
    st.session_state[f"{PAGE}.open_source"] = "No filter"
    st.session_state[f"{PAGE}.instruction_tuned"] = "True"
    st.session_state[f"{PAGE}.carbon_filter"] = "No filters"
    st.session_state[f"{PAGE}.min_carbon"] = 0.0
    st.session_state[f"{PAGE}.max_carbon"] = 10000.0
    st.session_state[f"{PAGE}.lan_llm"] = []
    st.session_state[f"{PAGE}.license"] = []
    
    # Display options
    st.session_state[f"{PAGE}.project_llm_multiselect"] = ["name", "version", "numberOfParameters", "instructionTuned"]
    st.session_state[f"{PAGE}.project_dt_multiselect"] = ["name", "description", "subTasks"]
    st.session_state[f"{PAGE}.project_metrics_multiselect"] = ["name", "description"]
    
    # Ranking options - pre-configured for Tabby metric ranking
    st.session_state[f"{PAGE}.rank_by"] = "Metric Score"
    st.session_state[f"{PAGE}.sort_order"] = "Descending (High to Low)"
    
    st.session_state[f"{PAGE}.initialized"] = True

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"
st.html(title_alignment)
st.image("static/6.png", use_column_width=True)

st.markdown("""
**Pre-configured Query:** *"Find instruction-tuned models under 8B parameters for code generation, ranked by a suitable metric."*

This query connects **Model**s to **Task**s and **Metric**s to **Model**s using two types of relationships:
- **suited_for** relationship: We use this link to retrieve models that are suited for specific downstream tasks
- **evaluates_model** relationship: We use this link to retrieve metrics that evaluate model performance, including the actual evaluation scores

The query applies the following pre-configured filters:
            
- **Model filters:** InstructionTuned=True, NumberOfParameters < 8B  
- **Task filters:** SubTask = Code Generation  
- **Metric filters:** Name = Tabby (suitable for code generation)
- **Ranking options:** Metric Score (descending, highest scores first)  
            
The filters are already applied in the sections below.
""")

# -----------------------------------------------------------------------------
# SECTION FOR DOWNSTREAM TASK FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html(f"<h3 style='text-align: center;'>{DOWNSTREAM_TASKS} filters</h3>")

col_dt1, col_dt2 = st.columns(2)
with col_dt1:
    st.multiselect(
        "**Downstream Task**",
        dao.get_all(DOWNSTREAM_TASKS, "name"),
        key=f"{PAGE}.assesses_downstream_task",
        default=st.session_state.get(f"{PAGE}.assesses_downstream_task", ["Code Generation"]),
        help="Select downstream tasks that the metrics are designed to assess."
    )

with col_dt2:
    # Show available task names for reference
    all_task_names = dao.get_all("Downstream Tasks", "name")
    st.info(f"Available tasks: {', '.join(all_task_names)}")

# Initialize downstream task filters
st.session_state[f"{PAGE}.filters_dt"] = {}

# Store downstream task metric assesses filter for later use in metrics filtering
if st.session_state[f"{PAGE}.assesses_downstream_task"]:
    st.session_state[f"{PAGE}.metric_assesses_filter"] = st.session_state[f"{PAGE}.assesses_downstream_task"]
else:
    st.session_state[f"{PAGE}.metric_assesses_filter"] = None

# -----------------------------------------------------------------------------
# SECTION FOR METRICS FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html("<h3 style='text-align: center;'>Metrics filters</h3>")
col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
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
    st.radio("**Context Free**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.contextFree")
    st.radio("**Trained**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.trained")
    st.radio("**Feature Based**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.featureBased")

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
    if st.session_state[f"{PAGE}.trained"] == "True":
        st.multiselect(
            "**Feature Based - End to End**",
            dao.get_all(METRICS, "featureBased/endToEnd"),
            key=f"{PAGE}.feat",
            default=st.session_state.get(f"{PAGE}.feat", [])
        )
    else:
        st.multiselect(
            "**Granularity**",
            dao.get_all(METRICS, "granularity"),
            key=f"{PAGE}.granularity",
            default=st.session_state.get(f"{PAGE}.granularity", [])
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
    st.multiselect(
        "**Metric Name**",
        dao.get_all(METRICS, "name"),
        key=f"{PAGE}.metric_name",
        default=st.session_state.get(f"{PAGE}.metric_name", ["Tabby"]),  # Pre-configured for Tabby
        help="Select specific metrics by name. Tabby is pre-selected as it's suitable for code generation."
    )

# Initialize metric filters
st.session_state[f"{PAGE}.filters_metrics"] = {}

# If specific metric names are selected, ONLY use the name filter (ignore all other filters)
if st.session_state[f"{PAGE}.metric_name"]:
    st.session_state[f"{PAGE}.filters_metrics"]["name"] = {"$in": st.session_state[f"{PAGE}.metric_name"]}
else:
    # Apply all filters when no specific metric name is selected
    if st.session_state[f"{PAGE}.contextFree"] != "No filter":
        st.session_state[f"{PAGE}.filters_metrics"]["contextFree"] = st.session_state[f"{PAGE}.contextFree"] == "True"

    if st.session_state[f"{PAGE}.trained"] != "No filter":
        st.session_state[f"{PAGE}.filters_metrics"]["trained"] = st.session_state[f"{PAGE}.trained"] == "True"

    if st.session_state[f"{PAGE}.featureBased"] != "No filter":
        st.session_state[f"{PAGE}.filters_metrics"]["featureBased"] = st.session_state[f"{PAGE}.featureBased"] == "True"

    # Apply additional filters only when no specific metric name is selected
    if st.session_state[f"{PAGE}.trained"] == "True" and st.session_state[f"{PAGE}.feat"]:
        st.session_state[f"{PAGE}.filters_metrics"]["featureBased.endToEnd"] = {"$in": st.session_state[f"{PAGE}.feat"]}
    elif st.session_state[f"{PAGE}.granularity"]:
        st.session_state[f"{PAGE}.filters_metrics"]["granularity"] = {"$in": st.session_state[f"{PAGE}.granularity"]}

    # Use the stored downstream task metric assesses filter from the downstream task section
    if st.session_state[f"{PAGE}.metric_assesses_filter"]:
        st.session_state[f"{PAGE}.filters_metrics"]["assessesDownstreamTask"] = {"$in": st.session_state[f"{PAGE}.metric_assesses_filter"]}

# -----------------------------------------------------------------------------
# SECTION FOR LARGE LANGUAGE MODEL FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html("<h3 style='text-align: center;'>Large Language Model filters</h3>")
col_m1, col_m2, col_m3, col_m4, col_m5, col_m6, col_m7, col_m8 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
)

with col_m1:
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

with col_m2:
    st.radio(
        "***Filter on Number of Parameters***",
        ["No filters", "Number of Parameters (B)"],
        key=f"{PAGE}.num_param_filter",
        index=1,  # Pre-select "Number of Parameters (B)"
    )
    if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
        st.number_input(
            "**Minimum number of parameters (B)**", min_value=0.0, value=0.0, step=0.1,
            key=f"{PAGE}.min_num_param",
        )
        st.number_input(
            "**Maximum number of parameters (B)**", min_value=0.0, value=8.0, step=0.1,
            key=f"{PAGE}.max_num_param",
        )

with col_m3:
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

with col_m4:
    # radio buttons for binary model attributes - pre-configured for instruction tuned
    st.radio("**Open Source**", ["No filter", "True", "False"], 
             index=0, key=f"{PAGE}.open_source")
    st.radio("**Instruction Tuned**", ["No filter", "True", "False"], 
             index=1, key=f"{PAGE}.instruction_tuned")  # Pre-select "True"
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

with col_m5:
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

with col_m6:
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
        default=st.session_state.get(f"{PAGE}.license", []),
    )

with col_m7:
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
# FINAL SECTION FOR QUERYING AND DISPLAY
# -----------------------------------------------------------------------------
st.markdown("---")
# Choose which fields to display from models, tasks, and metrics
st.multiselect(
    "**Select the results of the query for LLM**",
    dao.get_attributes(MODELS),
    st.session_state.get(f"{PAGE}.project_llm_multiselect", ["name", "version", "numberOfParameters", "instructionTuned"]),
    key=f"{PAGE}.project_llm_multiselect",
)

st.multiselect(
    "**Select the results of the query for Downstream Task**",
    dao.get_attributes(DOWNSTREAM_TASKS),
    st.session_state.get(f"{PAGE}.project_dt_multiselect", ["name", "description", "subTasks"]),
    key=f"{PAGE}.project_dt_multiselect",
)

st.multiselect(
    "**Select the results of the query for Metrics**",
    dao.get_attributes(METRICS),
    st.session_state.get(f"{PAGE}.project_metrics_multiselect", ["name", "description"]),
    key=f"{PAGE}.project_metrics_multiselect",
)

with st.expander("**📊 Ranking Options**", expanded=True):  # Expanded since ranking is key for this query
    st.radio(
        "**Rank by**",
        ["No ranking", "Model Parameters", "Model Carbon Emissions", "Metric Score"],
        index=3,  # Pre-select "Metric Score"
        key=f"{PAGE}.rank_by"
    )
    if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
        st.radio(
            "**Sort order**",
            ["Ascending (Low to High)", "Descending (High to Low)"],
            index=1,  # Pre-select "Descending" for highest scores first
            key=f"{PAGE}.sort_order"
        )

# Button to trigger the query
l, l1, c, r1, r = st.columns(5)
with c:
    query = st.button("Get results")

if query:
    # -------------------------------------------------------------------------
    # Build projection lists for all three entity types
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

    dt_project_fields = st.session_state[f"{PAGE}.project_dt_multiselect"].copy()
    if "_id" not in dt_project_fields:
        dt_project_fields.append("_id")

    metrics_project_fields = st.session_state[f"{PAGE}.project_metrics_multiselect"].copy()
    if "_id" not in metrics_project_fields:
        metrics_project_fields.append("_id")
    
    # If ranking by metric score, ensure we'll display score information
    # Note: Score comes from Edges collection, not Metrics, so we'll add it during result processing

    # -------------------------------------------------------------------------
    # Query all three collections with selected projection and filters
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
            if "Models" in item and "numberOfParameters" in item["Models"]:
                param_value = item["Models"]["numberOfParameters"]
            if param_value is not None:
                numeric_params = convert_params_to_numeric(param_value)
                if min_params <= numeric_params <= max_params:
                    filtered_models.append(item)
            elif min_params == 0:
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
                    pass
            elif min_carbon == 0:
                filtered_models.append(item)
        models_result = filtered_models

    # Query downstream tasks
    dt_query = create_query_structure(
        collection=DOWNSTREAM_TASKS,
        project=dt_project_fields,
        filters=st.session_state[f"{PAGE}.filters_dt"],
    )
    dt_result = dao.query([dt_query])

    # Query metrics
    metrics_query = create_query_structure(
        collection=METRICS,
        project=metrics_project_fields,
        filters=st.session_state[f"{PAGE}.filters_metrics"],
    )
    metrics_result = dao.query([metrics_query])

    # -------------------------------------------------------------------------
    # Query for the edges that create the three-way relationships
    edges_query = create_query_structure(
        collection="Edges",
        project=["from", "to", "relation_type", "score"],  # Include score field
        filters={"$or": [
            {"relation_type": "suited_for"},
            {"relation_type": "evaluates_model"}
        ]},
    )
    edges_result = dao.query([edges_query])

    # -------------------------------------------------------------------------
    # Create the three-way join: Model <-> Task (suited_for), Model <-> Metric (evaluates_model)
    # This creates triangular relationships where models are connected to both tasks and metrics
    joined_results = []
    
    # First, create a mapping of model relationships
    model_to_tasks = {}
    model_to_metrics = {}
    model_metric_scores = {}  # Store actual metric scores
    
    for edge in edges_result:
        if "Edges" not in edge:
            continue
        edge_data = edge["Edges"]
        relation_type = edge_data.get("relation_type")
        
        if relation_type == "suited_for":
            # Model -> Task relationship
            model_id = edge_data.get("from", "").replace("model:", "")
            task_id = edge_data.get("to", "").replace("task:", "")
            if model_id not in model_to_tasks:
                model_to_tasks[model_id] = []
            model_to_tasks[model_id].append(task_id)
            
        elif relation_type == "evaluates_model":
            # Metric -> Model relationship
            metric_id = edge_data.get("from", "").replace("metric:", "")  
            model_id = edge_data.get("to", "").replace("model:", "")
            score = edge_data.get("score")
            
            if model_id not in model_to_metrics:
                model_to_metrics[model_id] = []
            model_to_metrics[model_id].append(metric_id)
            
            # Store the actual score for this model-metric pair
            if model_id not in model_metric_scores:
                model_metric_scores[model_id] = {}
            model_metric_scores[model_id][metric_id] = score

    # Now create the final joined results by finding models that have both task and metric relationships
    for model in models_result:
        if "Models" not in model:
            continue
        model_id = model["Models"].get("_id", "").replace("model:", "")
        
        # Find associated tasks and metrics for this model
        associated_tasks = model_to_tasks.get(model_id, [])
        associated_metrics = model_to_metrics.get(model_id, [])
        
        # Only include models that have both task and metric relationships
        if associated_tasks and associated_metrics:
            # Find matching task and metric objects
            for task in dt_result:
                if "Downstream Tasks" not in task:
                    continue
                task_id = task["Downstream Tasks"].get("_id", "").replace("task:", "")
                if task_id in associated_tasks:
                    for metric in metrics_result:
                        if "Metrics" not in metric:
                            continue
                        metric_id = metric["Metrics"].get("_id", "").replace("metric:", "")
                        if metric_id in associated_metrics:
                            # Create a combined result with all three entities
                            joined_result = {**model, **task, **metric}
                            
                            # Add the actual metric score to the result
                            if model_id in model_metric_scores and metric_id in model_metric_scores[model_id]:
                                score = model_metric_scores[model_id][metric_id]
                                # Add score to a separate Evaluation section (like in trio_query.py)
                                joined_result["Evaluation"] = {"score": score}
                            
                            joined_results.append(joined_result)

    # -------------------------------------------------------------------------
    # Display the joined results
    if joined_results:
        # Apply ranking if selected
        if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
            def convert_params_to_numeric(param_str):
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
                if st.session_state[f"{PAGE}.rank_by"] == "Model Parameters":
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
                elif st.session_state[f"{PAGE}.rank_by"] == "Metric Score":
                    # Check if item has a valid metric score in Evaluation section
                    return "Evaluation" in item and "score" in item["Evaluation"] and item["Evaluation"]["score"] is not None
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
                elif st.session_state[f"{PAGE}.rank_by"] == "Metric Score":
                    # Use actual metric scores for ranking from Evaluation section
                    if "Evaluation" in item and "score" in item["Evaluation"]:
                        try:
                            return float(item["Evaluation"]["score"])
                        except (ValueError, TypeError):
                            return 0.0
                    return 0.0
                return 0
            
            # Filter out items with null/missing ranking values
            joined_results = [item for item in joined_results if has_valid_ranking_value(item)]
            
            # Sort the remaining items
            reverse_order = st.session_state[f"{PAGE}.sort_order"] == "Descending (High to Low)"
            joined_results = sorted(joined_results, key=get_sort_key, reverse=reverse_order)
        
        # Show success message with count
        st.success(f"Found {len(joined_results)} model-task-metric relationships matching your filters.")
        
        # If ranking is active, show information about the ranking
        if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
            st.info(f"Results are ranked by {st.session_state[f'{PAGE}.rank_by']} ({st.session_state[f'{PAGE}.sort_order']}).")
        
        df = pd.DataFrame(reworked_query_output(joined_results))
        st.dataframe(df)
        
        # Show summary of what was found
        model_names = set()
        task_names = set()
        metric_names = set()
        for result in joined_results:
            if "Models" in result:
                model_names.add(result["Models"].get("name", "Unknown"))
            if "Downstream Tasks" in result:
                task_names.add(result["Downstream Tasks"].get("name", "Unknown"))
            if "Metrics" in result:
                metric_names.add(result["Metrics"].get("name", "Unknown"))
        
        st.info(f"**Found Models:** {', '.join(sorted(model_names))}")
        st.info(f"**Found Tasks:** {', '.join(sorted(task_names))}")
        st.info(f"**Found Metrics:** {', '.join(sorted(metric_names))}")
    else:
        st.warning("No three-way relationships found matching the specified filters.")
        st.info("This means there are no models that are both suited for the selected tasks and evaluated by the selected metrics with the current filters.")
