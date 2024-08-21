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
st.image("static/llm.svg")

### SECTION FOR LARGE LANGUAGE MODEL ###

st.markdown("---")
st.html("<h2 style='text-align: center;'>Large Language Model filters</h2>")
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
    "$and": [
        {f"numberOfParameters [B]": {"$gte": st.session_state[f"{PAGE}.min_num_param"]}},
        {
            f"numberOfParameters [B]": {"$lte": 
                st.session_state[f"{PAGE}.max_num_param"] if st.session_state[f"{PAGE}.max_num_param"] else 1e9}
        },  # TODO: numero
    ],
    f"openSource": st.session_state[f"{PAGE}.open_source"],
    f"fineTuned": st.session_state[f"{PAGE}.fine_tuned"],
    # "quantization": quantization,  # FIXME: fixami
    f"contextLength": {"$gte": st.session_state[f"{PAGE}.cont_length"]},
}

if st.session_state[f"{PAGE}.arch"]:
    st.session_state[f"{PAGE}.filters_llm"][f"architecture"] = st.session_state[f"{PAGE}.arch"][0]

if st.session_state[f"{PAGE}.lan_llm"]:
    st.session_state[f"{PAGE}.filters_llm"][f"languages"] = {"$all": st.session_state[f"{PAGE}.lan_llm"]}


project_llm = st.multiselect(
    "**Select the results of the query from LLM**",
    dao.get_attributes(MODELS),
    ["name", "version", "numberOfParameters [B]"],
    key=f"{PAGE}.project_llm_multiselect"
)
st.session_state[f"{PAGE}.project_llm"] = st.session_state[f"{PAGE}.project_llm_multiselect"]

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=MODELS, 
        project=st.session_state[f"{PAGE}.project_llm"],
        filters=st.session_state[f"{PAGE}.filters_llm"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
