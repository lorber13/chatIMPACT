import streamlit as st
import pandas as pd
import json
import os
from utils import create_query_structure, reworked_query_output
from dao import Dao

# This Streamlit page provides a three-way combined view over Large Language Models (LLMs),
# Downstream Tasks, and Metrics. Users can apply filters to all three entity types and then
# correlate them through their relationships. The underlying database contains an ``Edges``
# collection where:
# - Entries with ``relation_type`` set to ``suited_for`` link a model to a task
# - Entries with ``relation_type`` set to ``evaluates_model`` link a metric to a model
# This creates a triangular relationship: Model <-> Task, Model <-> Metric

PAGE = "Trio"
DOWNSTREAM_TASKS = "Downstream Tasks"
MODELS = "Models"
METRICS = "Metrics"
DB_NAME = "ChatIMPACT"

# Initialise data access object
dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"
st.html(title_alignment)

# -----------------------------------------------------------------------------
# SECTION FOR DOWNSTREAM TASK FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html(f"<h3 style='text-align: center;'>{DOWNSTREAM_TASKS} filters</h3>")

col_dt1, col_dt2 = st.columns(2)
with col_dt1:
    st.multiselect(
        "**Downstream Task**",
        dao.get_all("Downstream Tasks", "name"),
        key=f"{PAGE}.name_dt",
        default=st.session_state[f"{PAGE}.name_dt"] if f"{PAGE}.name_dt" in st.session_state else None,
        help="Select specific downstream tasks to find models suited for them and their evaluation metrics."
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
# SECTION FOR METRICS FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html("<h3 style='text-align: center;'>Metrics filters</h3>")
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
            default=st.session_state[f"{PAGE}.feat"] if f"{PAGE}.feat" in st.session_state else None
        )
    else:
        st.multiselect(
            "**Granularity**",
            dao.get_all(METRICS, "granularity"),
            key=f"{PAGE}.granularity",
            default=st.session_state[f"{PAGE}.granularity"] if f"{PAGE}.granularity" in st.session_state else None
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
        "**Downstream Task Metric Assesses**",
        dao.get_all(DOWNSTREAM_TASKS, "name"),
        key=f"{PAGE}.assesses_downstream_task",
        default=st.session_state[f"{PAGE}.assesses_downstream_task"] if f"{PAGE}.assesses_downstream_task" in st.session_state else None
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

with col_8:
    st.multiselect(
        "**Metric Name**",
        dao.get_all(METRICS, "name"),
        key=f"{PAGE}.metric_name",
        default=st.session_state[f"{PAGE}.metric_name"] if f"{PAGE}.metric_name" in st.session_state else None,
        help="Select specific metrics by name to filter the results."
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

    if st.session_state[f"{PAGE}.assesses_downstream_task"]:
        st.session_state[f"{PAGE}.filters_metrics"]["assessesDownstreamTask"] = {"$in": st.session_state[f"{PAGE}.assesses_downstream_task"]}

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
    # radio buttons for binary model attributes
    st.radio("**Open Source**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.open_source")
    st.radio("**Instruction Tuned**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.instruction_tuned")
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
    st.radio(
        "***Filter on Context Length***",
        ["No filters", "Context Length"],
        key=f"{PAGE}.context_filter",
    )
    if st.session_state[f"{PAGE}.context_filter"] == "Context Length":
        st.number_input(
            "**Minimum context length**", min_value=0, value=0, step=1,
            key=f"{PAGE}.min_context",
        )
        st.number_input(
            "**Maximum context length**", min_value=0, value=1000000, step=1,
            key=f"{PAGE}.max_context",
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

with col_m8:
    # Additional model filters can be added here if needed
    pass

# Initialize model filters
st.session_state[f"{PAGE}.filters_models"] = {}

# Boolean filters for models
if st.session_state[f"{PAGE}.open_source"] != "No filter":
    st.session_state[f"{PAGE}.filters_models"]["openSource"] = st.session_state[f"{PAGE}.open_source"] == "True"

if st.session_state[f"{PAGE}.instruction_tuned"] != "No filter":
    st.session_state[f"{PAGE}.filters_models"]["instructionTuned"] = st.session_state[f"{PAGE}.instruction_tuned"] == "True"

# Numeric range filters for models
if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
    min_param = st.session_state[f"{PAGE}.min_num_param"]
    max_param = st.session_state[f"{PAGE}.max_num_param"]
    if min_param > 0 or max_param < 1000:
        # Convert parameter values for comparison
        param_filter = {}
        if min_param > 0:
            param_filter["$gte"] = f"{min_param}B"
        if max_param < 1000:
            param_filter["$lte"] = f"{max_param}B"
        if param_filter:
            st.session_state[f"{PAGE}.filters_models"]["numberOfParameters"] = param_filter

if st.session_state[f"{PAGE}.carbon_filter"] == "Carbon Emissions (tCO2e)":
    min_carbon = st.session_state[f"{PAGE}.min_carbon"]
    max_carbon = st.session_state[f"{PAGE}.max_carbon"]
    if min_carbon > 0 or max_carbon < 10000:
        carbon_filter = {}
        if min_carbon > 0:
            carbon_filter["$gte"] = min_carbon
        if max_carbon < 10000:
            carbon_filter["$lte"] = max_carbon
        if carbon_filter:
            st.session_state[f"{PAGE}.filters_models"]["carbon_emissions_tco2e"] = carbon_filter

if st.session_state[f"{PAGE}.context_filter"] == "Context Length":
    min_context = st.session_state[f"{PAGE}.min_context"]
    max_context = st.session_state[f"{PAGE}.max_context"]
    if min_context > 0 or max_context < 1000000:
        context_filter = {}
        if min_context > 0:
            context_filter["$gte"] = min_context
        if max_context < 1000000:
            context_filter["$lte"] = max_context
        if context_filter:
            st.session_state[f"{PAGE}.filters_models"]["contextLength"] = context_filter

# Array-based filters for models - removed input/output modalities as requested

# -----------------------------------------------------------------------------
# RANKING SECTION
# -----------------------------------------------------------------------------
st.markdown("---")
with st.expander("**📊 Ranking Options**", expanded=False):
    st.selectbox(
        "**Rank by:**",
        ["No ranking", "Evaluation Score", "Model Parameters", "Model Carbon Emissions"],
        index=0,
        key=f"{PAGE}.rank_by"
    )
    
    if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
        st.radio(
            "**Order:**",
            ["Ascending", "Descending"],
            index=1,  # Default to descending
            key=f"{PAGE}.order"
        )

# -----------------------------------------------------------------------------
# QUERY EXECUTION BUTTON
# -----------------------------------------------------------------------------
st.markdown("---")
if st.button("**Get results**", key=f"{PAGE}.submit"):
    
    # Add ranking fields to project if ranking is active
    base_models_project = [
        "_id", "name", "huggingFaceId", "openSource", "instructionTuned",
        "numberOfParameters", "contextLength", "carbon_emissions_tco2e"
    ]
    base_metrics_project = [
        "_id", "name", "contextFree", "trained", "featureBased", "granularity",
        "assessesDownstreamTask"
    ]
    base_tasks_project = ["_id", "name", "description"]
    
    # Add ranking fields to projections if needed
    models_project = base_models_project.copy()
    metrics_project = base_metrics_project.copy()
    tasks_project = base_tasks_project.copy()

    # Query downstream tasks - if no specific tasks selected, get all tasks
    if st.session_state[f"{PAGE}.filters_dt"]:
        task_query = create_query_structure(
            collection=DOWNSTREAM_TASKS,
            project=tasks_project,
            filters=st.session_state[f"{PAGE}.filters_dt"],
        )
    else:
        # Get all tasks if no specific filter
        task_query = create_query_structure(
            collection=DOWNSTREAM_TASKS,
            project=tasks_project,
            filters={},
        )
    tasks_result = dao.query([task_query])

    # Query metrics - use direct equality instead of $in for single values
    if st.session_state.get(f"{PAGE}.metric_name") and len(st.session_state[f"{PAGE}.metric_name"]) == 1:
        # For single metric selection, use direct equality
        metrics_query = create_query_structure(
            collection=METRICS,
            project=metrics_project,
            filters={"name": st.session_state[f"{PAGE}.metric_name"][0]},
        )
    else:
        # For multiple metrics or other filters, use the original logic
        metrics_query = create_query_structure(
            collection=METRICS,
            project=metrics_project,
            filters=st.session_state[f"{PAGE}.filters_metrics"],
        )
    metrics_result = dao.query([metrics_query])

    # Query models
    models_query = create_query_structure(
        collection=MODELS,
        project=models_project,
        filters=st.session_state[f"{PAGE}.filters_models"],
    )
    models_result = dao.query([models_query])

    # Load edges directly from JSON file since database doesn't contain edges
    import json
    import os
    
    edges_file_path = os.path.join(os.path.dirname(__file__), "..", "local_data", "Edges.json")
    try:
        with open(edges_file_path, 'r') as f:
            all_edges_data = json.load(f)
        
        # Filter for suited_for edges
        suited_for_edges_result = []
        for edge in all_edges_data:
            if edge.get("relation_type") == "suited_for":
                # Wrap in Edges structure to match expected format
                suited_for_edges_result.append({"Edges": edge})
        
        # Filter for evaluates_model edges
        evaluates_model_edges_result = []
        for edge in all_edges_data:
            if edge.get("relation_type") == "evaluates_model":
                # Wrap in Edges structure to match expected format
                evaluates_model_edges_result.append({"Edges": edge})
                
    except FileNotFoundError:
        st.error("Edges.json file not found. Please check the file path.")
        suited_for_edges_result = []
        evaluates_model_edges_result = []

    # -------------------------------------------------------------------------
    # Three-way join: Model <-> Task (via suited_for) AND Model <-> Metric (via evaluates_model)
    # -------------------------------------------------------------------------
    
    # Create task name to ID mapping
    task_name_to_id = {}
    for task in tasks_result:
        if "Downstream Tasks" in task:
            task_data = task["Downstream Tasks"]
            task_name = task_data.get("name", "")
            task_id = task_data.get("_id", "").replace("task:", "")
            if task_name:
                task_name_to_id[task_name] = task_id

    joined_results = []
    
    # Process suited_for edges first to establish model-task pairs
    model_task_pairs = []
    for edge in suited_for_edges_result:
        if "Edges" not in edge:
            continue
        edge_data = edge["Edges"]
        model_id = edge_data.get("from", "").replace("model:", "")
        task_ref = edge_data.get("to", "").replace("task:", "")
        
        # Find matching task - handle both ID and name references
        matching_task = None
        for task in tasks_result:
            if "Downstream Tasks" in task:
                task_data = task["Downstream Tasks"]
                current_id = task_data.get("_id", "").replace("task:", "")
                current_name = task_data.get("name", "")
                
                # Check if edge references task by ID or name
                if current_id == task_ref or current_name == task_ref:
                    matching_task = task
                    break

        # Find matching model
        matching_model = None
        for model in models_result:
            if "Models" in model:
                current_id = model["Models"].get("_id", "").replace("model:", "")
                if current_id == model_id:
                    matching_model = model
                    break

        if matching_task and matching_model:
            model_task_pairs.append({
                'model': matching_model,
                'task': matching_task,
                'model_id': model_id
            })

    # Now add metrics to the model-task pairs via evaluates_model edges
    for model_task_pair in model_task_pairs:
        model_id = model_task_pair['model_id']
        
        # Find all metrics that evaluate this model
        for edge in evaluates_model_edges_result:
            if "Edges" not in edge:
                continue
            edge_data = edge["Edges"]
            metric_id = edge_data.get("from", "").replace("metric:", "")
            evaluated_model_id = edge_data.get("to", "").replace("model:", "")
            score = edge_data.get("score", None)
            
            if evaluated_model_id == model_id:
                # Find matching metric
                matching_metric = None
                for metric in metrics_result:
                    if "Metrics" in metric:
                        current_id = metric["Metrics"].get("_id", "").replace("metric:", "")
                        if current_id == metric_id:
                            matching_metric = metric
                            break

                if matching_metric:
                    # Create three-way joined result
                    joined_result = {
                        **model_task_pair['model'], 
                        **model_task_pair['task'], 
                        **matching_metric
                    }
                    if score is not None:
                        joined_result["Evaluation"] = {"score": score}
                    joined_results.append(joined_result)


    # -------------------------------------------------------------------------
    # Apply ranking and display results
    # -------------------------------------------------------------------------
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
            
            def has_valid_ranking_value(item):
                """Check if item has a valid (non-null) value for the selected ranking field"""
                if st.session_state[f"{PAGE}.rank_by"] == "Evaluation Score":
                    return "Evaluation" in item and "score" in item["Evaluation"] and item["Evaluation"]["score"] is not None
                elif st.session_state[f"{PAGE}.rank_by"] == "Model Parameters":
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
                return True
            
            def get_ranking_value(item):
                """Extract the numeric value for ranking"""
                if st.session_state[f"{PAGE}.rank_by"] == "Evaluation Score":
                    return item["Evaluation"]["score"]
                elif st.session_state[f"{PAGE}.rank_by"] == "Model Parameters":
                    param_value = item["Models"]["numberOfParameters"]
                    return convert_params_to_numeric(param_value)
                elif st.session_state[f"{PAGE}.rank_by"] == "Model Carbon Emissions":
                    return float(item["Models"]["carbon_emissions_tco2e"])
                return 0
            
            # Filter out items with null/missing ranking values
            joined_results = [item for item in joined_results if has_valid_ranking_value(item)]
            
            # Sort by the selected field
            reverse_order = st.session_state[f"{PAGE}.order"] == "Descending"
            joined_results.sort(key=get_ranking_value, reverse=reverse_order)
        
        # Display the results
        st.success(f"Found {len(joined_results)} matching model-task-metric combinations!")
        df = pd.DataFrame(reworked_query_output(joined_results))
        st.dataframe(df)
    else:
        st.warning("No matching model-task-metric combinations found with the current filters.")
        
        # Provide helpful suggestions
        if len(metrics_result) == 0:
            st.info("❗ No metrics match your metric filters. Try relaxing the metric constraints.")
        elif len(models_result) == 0:
            st.info("❗ No models match your model filters. Try relaxing the model constraints.")
        elif len(tasks_result) == 0 and st.session_state[f"{PAGE}.name_dt"]:
            st.info("❗ No tasks match your task filter. Try selecting different tasks or leave the task filter empty.")
        elif len(model_task_pairs) == 0:
            st.info("❗ No model-task relationships found. The selected models and tasks may not be connected via 'suited_for' relationships.")
        else:
            st.info("❗ No metric-model evaluation relationships found for the selected combinations. Try different filters or check if the selected metrics evaluate the selected models.")
            
            # Show specific suggestions for Tabby metric
            tabby_selected = False
            for metric in metrics_result:
                if "Metrics" in metric and metric["Metrics"].get("name", "").lower() == "tabby":
                    tabby_selected = True
                    break
            
            if tabby_selected:
                st.info("💡 **Tip for Tabby metric**: Tabby evaluates code generation models. Try selecting 'Code Generation' as the downstream task or remove task filters to see all Tabby evaluations.")
