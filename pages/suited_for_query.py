import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Suited For"
DOWNSTREAM_TASKS = "Downstream Tasks"
MODELS = "Models"
DB_NAME = "ChatIMPACT"

dao = Dao("ChatIMPACT")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
st.image("static/suited_for.svg")

### SECTION FOR DOWNSTREAM TASKS ###
st.html(f"<h3 style='text-align: center;'>{DOWNSTREAM_TASKS} filters</h3>")
st.multiselect(
    "**Downstream Task**",
    dao.get_all("Downstream Tasks", "name"),
    key=f"{PAGE}.name_dt",
    default=st.session_state[f"{PAGE}.name_dt"] if f"{PAGE}.name_dt" in st.session_state else None
)
st.session_state[f"{PAGE}.filters_dt"] = {}

if st.session_state[f"{PAGE}.name_dt"]:
    st.session_state[f"{PAGE}.filters_dt"][f"{DOWNSTREAM_TASKS}.name"] = st.session_state[f"{PAGE}.name_dt"][0]

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
            "**Minimum number of parameters**", min_value=0, value=0,
            key=f"{PAGE}.min_num_param"
        )
        st.number_input(
            "**Maximum number of parameters**", min_value=0, value=None,
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
    st.toggle("**Fine-Tuned**", value=False, key=f"{PAGE}.fine_tuned")
    #quantization = st.toggle("**Quantization**", value=False)
    st.number_input(
        "**Minimum context length**",
        min_value=0,
        key=f"{PAGE}.cont_length"
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
        "**Architecture**",
        dao.get_all("Models", "architecture"),
        key=f"{PAGE}.arch",
        default=st.session_state[f"{PAGE}.arch"] if f"{PAGE}.arch" in st.session_state else None
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
    f"{MODELS}.openSource": st.session_state[f"{PAGE}.open_source"],
    f"{MODELS}.fineTuned": st.session_state[f"{PAGE}.fine_tuned"],
    # "quantization": quantization,  # FIXME: fixami
    f"{MODELS}.contextLength": {"$gte": st.session_state[f"{PAGE}.cont_length"]},
}

if st.session_state[f"{PAGE}.num_param_filter"] == "Number of Parameters (B)":
    st.session_state[f"{PAGE}.filters_llm"]["$and"] = [
        {f"{MODELS}.numberOfParameters [B]": {"$gte": st.session_state[f"{PAGE}.min_num_param"]}},
        {
            f"{MODELS}.numberOfParameters [B]": {"$lte": 
                st.session_state[f"{PAGE}.max_num_param"] if st.session_state[f"{PAGE}.max_num_param"] else 1e9}
        },  # TODO: numero
    ]

if st.session_state[f"{PAGE}.arch"]:
    st.session_state[f"{PAGE}.filters_llm"][f"{MODELS}.architecture"] = st.session_state[f"{PAGE}.arch"]

if st.session_state[f"{PAGE}.lan_llm"]:
    st.session_state[f"{PAGE}.filters_llm"][f"{MODELS}.languages"] = {"$all": st.session_state[f"{PAGE}.lan_llm"]}

### FINAL SECTION FOR QUERYING
st.markdown("---")
st.multiselect(
    "**Select the results of the query for Downstream Task**",
    dao.get_attributes(DOWNSTREAM_TASKS),
    ["name"],
    key=f"{PAGE}.project_dt_multiselect"
)
st.session_state[f"{PAGE}.project_dt"] = [f"{DOWNSTREAM_TASKS}." + att for att in st.session_state[f"{PAGE}.project_dt_multiselect"]]

st.multiselect(
    "**Select the results of the query for LLM**",
    dao.get_attributes(MODELS),
    ["name", "version", "numberOfParameters [B]"],
    key=f"{PAGE}.project_llm_multiselect"
)
st.session_state[f"{PAGE}.project_llm"] = [f"{MODELS}." + att for att in st.session_state[f"{PAGE}.project_llm_multiselect"]]


l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=DOWNSTREAM_TASKS, 
        project=st.session_state[f"{PAGE}.project_dt"], 
        filters=st.session_state[f"{PAGE}.filters_dt"]
    ),
    create_query_structure(
        collection=MODELS, 
        project=st.session_state[f"{PAGE}.project_llm"], 
        filters=st.session_state[f"{PAGE}.filters_llm"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)