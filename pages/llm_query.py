import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Large Language Model"
MODELS = "Models"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
st.image("static/llm.png", use_column_width=True)

### SECTION FOR LARGE LANGUAGE MODEL ###

st.markdown("---")
st.html("<h3 style='text-align: center;'>Large Language Model filters</h3>")
col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
)

with col_1:
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
        key=f"{PAGE}.num_param_filter"
    )
    if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
        st.number_input(
            "**Minimum number of parameters (B)**", min_value=0.0, value=0.0, step=0.1,
            key=f"{PAGE}.min_num_param"
        )
        st.number_input(
            "**Maximum number of parameters (B)**", min_value=0.0, value=1000.0, step=0.1,
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
    st.toggle("**Open Source**", value=False, key=f"{PAGE}.open_source")
    st.toggle("**Instruction Tuned**", value=False, key=f"{PAGE}.instruction_tuned")
    st.radio(
        "***Filter on Carbon Emissions***",
        ["No filters", "Carbon Emissions (tCO2e)"],
        key=f"{PAGE}.carbon_filter"
    )
    if st.session_state[f"{PAGE}.carbon_filter"] == "Carbon Emissions (tCO2e)":
        st.number_input(
            "**Minimum emissions (tCO2e)**", min_value=0.0, value=0.0, step=0.1,
            key=f"{PAGE}.min_carbon"
        )
        st.number_input(
            "**Maximum emissions (tCO2e)**", min_value=0.0, value=10000.0, step=0.1,
            key=f"{PAGE}.max_carbon"
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
        "**Language**",
        dao.get_all("Models", "languages"),
        key=f"{PAGE}.lan_llm",
        default=st.session_state[f"{PAGE}.lan_llm"] if f"{PAGE}.lan_llm" in st.session_state else None
    )
    st.multiselect(
        "**License to Use**",
        dao.get_all("Models", "license_to_use"),
        key=f"{PAGE}.license",
        default=st.session_state[f"{PAGE}.license"] if f"{PAGE}.license" in st.session_state else None
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

st.session_state[f"{PAGE}.filters_llm"] = {
    f"openSource": st.session_state[f"{PAGE}.open_source"],
    # "quantization": quantization,  # FIXME: fixami
    # Note: contextLength field not available in current data
}

# Only add instructionTuned filter if the toggle is True (since some models don't have this field)
if st.session_state[f"{PAGE}.instruction_tuned"]:
    st.session_state[f"{PAGE}.filters_llm"]["instructionTuned"] = True

st.session_state[f"{PAGE}.param_filter_active"] = False
st.session_state[f"{PAGE}.carbon_filter_active"] = False

if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
    # Convert string parameter counts to numeric values for comparison
    def convert_params_to_numeric(param_str):
        """Convert parameter strings like '7B', '176B' to numeric values in billions"""
        if not param_str:
            return 0
        param_str = str(param_str).upper()
        if param_str.endswith('B'):
            return float(param_str[:-1])
        elif param_str.endswith('M'):
            return float(param_str[:-1]) / 1000  # Convert millions to billions
        else:
            try:
                return float(param_str)
            except:
                return 0
    
    # Create a filter that works with string-based parameters
    min_params = st.session_state[f"{PAGE}.min_num_param"]
    max_params = st.session_state[f"{PAGE}.max_num_param"] if st.session_state[f"{PAGE}.max_num_param"] else 1e9
    
    # We'll need to handle this filtering in the application layer since MongoDB
    # can't directly compare these string formats numerically
    st.session_state[f"{PAGE}.param_filter_active"] = True
    st.session_state[f"{PAGE}.min_params"] = min_params
    st.session_state[f"{PAGE}.max_params"] = max_params

if st.session_state[f"{PAGE}.carbon_filter"] == "Carbon Emissions (tCO2e)":
    # Carbon emissions filtering (numeric values)
    min_carbon = st.session_state[f"{PAGE}.min_carbon"]
    max_carbon = st.session_state[f"{PAGE}.max_carbon"] if st.session_state[f"{PAGE}.max_carbon"] else 1e9
    
    # We'll handle this filtering in the application layer
    st.session_state[f"{PAGE}.carbon_filter_active"] = True
    st.session_state[f"{PAGE}.min_carbon_val"] = min_carbon
    st.session_state[f"{PAGE}.max_carbon_val"] = max_carbon

if st.session_state[f"{PAGE}.lan_llm"]:
    st.session_state[f"{PAGE}.filters_llm"][f"languages"] = {"$all": st.session_state[f"{PAGE}.lan_llm"]}

if st.session_state[f"{PAGE}.license"]:
    st.session_state[f"{PAGE}.filters_llm"][f"license_to_use"] = {"$all": st.session_state[f"{PAGE}.license"]}


st.multiselect(
    "**Select the results of the query**",
    dao.get_attributes(MODELS),
    ["name", "version", "numberOfParameters"],
    key=f"{PAGE}.project_llm_multiselect"
)
st.session_state[f"{PAGE}.project_llm"] = st.session_state[f"{PAGE}.project_llm_multiselect"]

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    # Ensure required fields are included in projection if filtering is active
    project_fields = st.session_state[f"{PAGE}.project_llm"].copy()
    if st.session_state.get(f"{PAGE}.param_filter_active", False) and "numberOfParameters" not in project_fields:
        project_fields.append("numberOfParameters")
    if st.session_state.get(f"{PAGE}.carbon_filter_active", False) and "carbon_emissions_tco2e" not in project_fields:
        project_fields.append("carbon_emissions_tco2e")
    
    query_input = [create_query_structure(
        collection=MODELS, 
        project=project_fields,
        filters=st.session_state[f"{PAGE}.filters_llm"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    
    # Apply parameter filtering if active
    if st.session_state.get(f"{PAGE}.param_filter_active", False):
        def convert_params_to_numeric(param_str):
            """Convert parameter strings like '7B', '176B' to numeric values in billions"""
            if not param_str:
                return 0
            param_str = str(param_str).upper()
            if param_str.endswith('B'):
                return float(param_str[:-1])
            elif param_str.endswith('M'):
                return float(param_str[:-1]) / 1000  # Convert millions to billions
            else:
                try:
                    return float(param_str)
                except:
                    return 0
        
        min_params = st.session_state[f"{PAGE}.min_params"]
        max_params = st.session_state[f"{PAGE}.max_params"]
        
        # Filter results based on numeric parameter comparison
        filtered_result = []
        
        for item in result:
            # Access numberOfParameters from the correct nested structure
            param_value = None
            if 'Models' in item and 'numberOfParameters' in item['Models']:
                param_value = item['Models']['numberOfParameters']
            
            if param_value is not None:
                numeric_params = convert_params_to_numeric(param_value)
                if min_params <= numeric_params <= max_params:
                    filtered_result.append(item)
            elif min_params == 0:  # Include items without numberOfParameters if min is 0
                filtered_result.append(item)
        
        result = filtered_result
    
    # Apply carbon emissions filtering if active
    if st.session_state.get(f"{PAGE}.carbon_filter_active", False):
        min_carbon = st.session_state[f"{PAGE}.min_carbon_val"]
        max_carbon = st.session_state[f"{PAGE}.max_carbon_val"]
        
        # Filter results based on carbon emissions comparison
        filtered_result = []
        
        for item in result:
            # Access carbon_emissions_tco2e from the correct nested structure
            carbon_value = None
            if 'Models' in item and 'carbon_emissions_tco2e' in item['Models']:
                carbon_value = item['Models']['carbon_emissions_tco2e']
            
            if carbon_value is not None:
                try:
                    numeric_carbon = float(carbon_value)
                    if min_carbon <= numeric_carbon <= max_carbon:
                        filtered_result.append(item)
                except:
                    # If conversion fails, skip this item
                    pass
            elif min_carbon == 0:  # Include items without carbon emissions if min is 0
                filtered_result.append(item)
        
        result = filtered_result
    
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
