import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

# This Streamlit page provides a combined view over Metrics and Large Language Models (LLMs).
# Users can apply filters to both metrics and models and then correlate them through their
# evaluation relationships. The underlying database contains an ``Edges`` collection where
# entries with ``relation_type`` set to ``evaluates_model`` link a metric (via the ``from``
# field) to a model (via the ``to`` field) with an optional score. The interface below
# retrieves and displays only those metric–model pairs that satisfy the selected filters
# on both sides and appear in the ``evaluates_model`` edges.

PAGE = "Evaluate"
METRICS = "Metrics"
MODELS = "Models"
DB_NAME = "ChatIMPACT"

# Initialise data access object
dao = Dao(DB_NAME)

# Page navigation and title
st.page_link("gui.py", label="Homepage", icon="🏠")
title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"
st.html(title_alignment)

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
            key=f"{PAGE}.gran",
            default=st.session_state[f"{PAGE}.gran"] if f"{PAGE}.gran" in st.session_state else None
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
    # additional metric filters can be added here
    st.multiselect(
        "**Context**",
        dao.get_all(METRICS, "context"),
        key=f"{PAGE}.context",
        default=st.session_state[f"{PAGE}.context"] if f"{PAGE}.context" in st.session_state else None
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

# Initialise filters for Metrics
st.session_state[f"{PAGE}.filters_metrics"] = {}

# Add filters only if not "No filter"
if st.session_state[f"{PAGE}.trained"] != "No filter":
    st.session_state[f"{PAGE}.filters_metrics"]["trained"] = st.session_state[f"{PAGE}.trained"] == "True"
if st.session_state[f"{PAGE}.contextFree"] != "No filter":
    st.session_state[f"{PAGE}.filters_metrics"]["contextFree"] = st.session_state[f"{PAGE}.contextFree"] == "True"
if st.session_state[f"{PAGE}.featureBased"] != "No filter":
    st.session_state[f"{PAGE}.filters_metrics"]["featureBased"] = st.session_state[f"{PAGE}.featureBased"] == "True"

if st.session_state[f"{PAGE}.context"]:
    st.session_state[f"{PAGE}.filters_metrics"]["context"] = {
        "$all": st.session_state[f"{PAGE}.context"]
    }

if st.session_state[f"{PAGE}.trained"] == "False":
    if st.session_state[f"{PAGE}.gran"]:
        st.session_state[f"{PAGE}.filters_metrics"]["granularity"] = {
            "$all": st.session_state[f"{PAGE}.gran"]
        }
if st.session_state[f"{PAGE}.trained"] == "True":
    if st.session_state[f"{PAGE}.feat"]:
        st.session_state[f"{PAGE}.filters_metrics"]["featureBased/endToEnd"] = {
            "$all": st.session_state[f"{PAGE}.feat"]
        }

# -----------------------------------------------------------------------------
# SECTION FOR MODEL FILTERS
# -----------------------------------------------------------------------------
st.markdown("---")
st.html("<h3 style='text-align: center;'>Large Language Model filters</h3>")
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
    # multi‑select fields for categorical attributes
    st.multiselect(
        "**Language**",
        dao.get_all("Models", "languages"),
        key=f"{PAGE}.lan_llm",
        default=st.session_state[f"{PAGE}.lan_llm"] if f"{PAGE}.lan_llm" in st.session_state else None,
    )
    st.multiselect(
        "**License to Use**",
        dao.get_all("Models", "license_to_use"),
        key=f"{PAGE}.license",
        default=st.session_state[f"{PAGE}.license"] if f"{PAGE}.license" in st.session_state else None,
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

# Initialise filters for Models
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
# Choose which fields to display from metrics and models
st.multiselect(
    "**Select the results of the query for Metrics**",
    dao.get_attributes(METRICS),
    ["name", "description"],
    key=f"{PAGE}.project_metrics_multiselect",
)

st.multiselect(
    "**Select the results of the query for Models**",
    dao.get_attributes(MODELS),
    ["name", "version", "numberOfParameters"],
    key=f"{PAGE}.project_llm_multiselect",
)

with st.expander("**📊 Ranking Options**", expanded=False):
    st.radio(
        "**Rank by**",
        ["No ranking", "Model Parameters", "Model Carbon Emissions", "Evaluation Score"],
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
    # Build projection lists, ensuring fields needed for manual filtering and
    # ranking are included when the corresponding filters/ranking are active.
    metrics_project_fields = st.session_state[f"{PAGE}.project_metrics_multiselect"].copy()
    
    # Always include _id for joining with edges
    if "_id" not in metrics_project_fields:
        metrics_project_fields.append("_id")

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

    # -------------------------------------------------------------------------
    # Query metrics collection with selected projection and filters
    metrics_query = create_query_structure(
        collection=METRICS,
        project=metrics_project_fields,
        filters=st.session_state[f"{PAGE}.filters_metrics"],
    )
    metrics_result = dao.query([metrics_query])

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
    # Retrieve all evaluates_model edges from the Edges collection. 
    # These records describe which metric evaluates which model with what score.
    
    edges_query = create_query_structure(
        collection="Edges",
        project=["from", "to", "relation_type", "score"],
        filters={"relation_type": "evaluates_model"},
    )
    edges_result = dao.query([edges_query])

    # -------------------------------------------------------------------------
    # Combine metrics and models according to the edges. Only those pairs
    # passing their respective filters will be displayed. We strip the
    # ``metric:`` and ``model:`` prefixes when comparing IDs because the
    # underlying entries in the Metrics and Models collections do not include
    # these prefixes in their ``_id`` fields.
    joined_results = []
    for edge in edges_result:
        if "Edges" not in edge:
            continue
        edge_data = edge["Edges"]
        metric_id = edge_data.get("from", "").replace("metric:", "")
        model_id = edge_data.get("to", "").replace("model:", "")
        score = edge_data.get("score", None)
        
        # find matching metric
        matching_metric = None
        for metric in metrics_result:
            if "Metrics" in metric:
                current_id = metric["Metrics"].get("_id", "").replace("metric:", "")
                if current_id == metric_id:
                    matching_metric = metric
                    break

        # find matching model
        matching_model = None
        for model in models_result:
            if "Models" in model:
                current_id = model["Models"].get("_id", "").replace("model:", "")
                if current_id == model_id:
                    matching_model = model
                    break

        # if both sides match, combine
        if matching_metric and matching_model:
            # merge dictionaries and add score from edge under an "Evaluation" collection
            joined_result = {**matching_metric, **matching_model}
            if score is not None:
                joined_result["Evaluation"] = {"score": score}
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
                elif st.session_state[f"{PAGE}.rank_by"] == "Evaluation Score":
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
                elif st.session_state[f"{PAGE}.rank_by"] == "Evaluation Score":
                    if "Evaluation" in item and "score" in item["Evaluation"]:
                        try:
                            return float(item["Evaluation"]["score"])
                        except (ValueError, TypeError):
                            return 0
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
            "No evaluation relationships found matching the specified filters."
        )
