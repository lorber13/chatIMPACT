import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Train"
MODELS = "Models"
DATASETS = "Datasets"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
st.image("static/train.svg")

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

### SECTION FOR DATASET ###

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
        ["No filters", "Disk space (GB)"],
        key=f"{PAGE}.type_filter"
    )
    if st.session_state[f"{PAGE}.type_filter"] == "Disk space (GB)":
        st.number_input(
            "**Minimum size [GB]**", min_value=0, value=0,
            key=f"{PAGE}.min_size_gb"
        )
        st.number_input(
            "**Maximum size [GB]**", min_value=0, value=None,
            key=f"{PAGE}.max_size_gb"
        )
    #if type_filter == "Row count":
    #    min_size_rows = st.number_input(
    #        "**Minimum size [rows]**", min_value=0, value=0
    #    )
    #    max_size_rows = st.number_input(
    #        "**Maximum size [rows]**", min_value=0, value=None
    #    )

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
    st.toggle("**Fine-Tuning Dataset**", 
              value=None,
              key=f"{PAGE}.fine_tuning")
    st.multiselect(
        "**Domain**",
        dao.get_all("Datasets", "domain"),
        key=f"{PAGE}.domain",
        default=st.session_state[f"{PAGE}.domain"] if f"{PAGE}.domain" in st.session_state else None
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
    st.multiselect(
        "**Language**",
        dao.get_all("Datasets", "languages"),
        key=f"{PAGE}.lan_ds",
        default=st.session_state[f"{PAGE}.lan_ds"] if f"{PAGE}.lan_ds" in st.session_state else None
    )
    st.multiselect(
        "**LicenseToUse**",
        dao.get_all("Datasets", "licenseToUse"),
        key=f"{PAGE}.lic",
        default=st.session_state[f"{PAGE}.lic"] if f"{PAGE}.lic" in st.session_state else None
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

st.session_state[f"{PAGE}.filters_ds"] = {}

if st.session_state[f"{PAGE}.type_filter"] == "Disk space (GB)":
    st.session_state[f"{PAGE}.filters_ds"]["$and"] = [
        {f"{DATASETS}.size [GB]": {"$gte": st.session_state[f"{PAGE}.min_size_gb"]}},
        {
            f"{DATASETS}.size [GB]": {"$lte": st.session_state[f"{PAGE}.max_size_gb"] if \
                                      st.session_state[f"{PAGE}.max_size_gb"] else 1e9}
        },  # TODO: numero
    ]

#if type_filter == "Row count":
#    filters_ds["$and"] = [
#        {f"{DATASETS}.size [rows]": {"$gte": min_size_rows}},
#        {
#            f"{DATASETS}.size [rows]": {"$lte": max_size_rows if max_size_rows else 1e9}
#        },  # TODO: numero
#    ]

if st.session_state[f"{PAGE}.fine_tuning"] is not None:
    st.session_state[f"{PAGE}.filters_ds"][f"{DATASETS}.fineTuning"] = st.session_state[f"{PAGE}.fine_tuning"]

if st.session_state[f"{PAGE}.domain"]:
    st.session_state[f"{PAGE}.filters_ds"][f"{DATASETS}.domain"] = {
        "$all": st.session_state[f"{PAGE}.domain"]
    }

if st.session_state[f"{PAGE}.lic"]:
    st.session_state[f"{PAGE}.filters_ds"][f"{DATASETS}.licenseToUse"] = {
        "$all": st.session_state[f"{PAGE}.lic"]
    }

if st.session_state[f"{PAGE}.lan_ds"]:
    st.session_state[f"{PAGE}.filters_ds"][f"{DATASETS}.languages"] = {
        "$all": st.session_state[f"{PAGE}.lan_ds"]
    }

### FINAL SECTION FOR QUERYING
st.markdown("---")
st.multiselect(
    "**Select the results of the query for LLM**",
    dao.get_attributes(MODELS),
    ["name", "version", "numberOfParameters [B]"],
    key=f"{PAGE}.project_llm_multiselect"
)
st.session_state[f"{PAGE}.project_llm"] = [f"{MODELS}." + att for att in st.session_state[f"{PAGE}.project_llm_multiselect"]]

st.multiselect(
    "**Select the results of the query for Dataset**",
    dao.get_attributes(DATASETS),
    ["name", "uri", "domain"],
    key=f"{PAGE}.project_ds_multiselect"
)
st.session_state[f"{PAGE}.project_ds"] = [f"{DATASETS}." + att for att in st.session_state[f"{PAGE}.project_ds_multiselect"]]


l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=MODELS, 
        project=st.session_state[f"{PAGE}.project_llm"], 
        filters=st.session_state[f"{PAGE}.filters_llm"]
    ),
    create_query_structure(
        collection=DATASETS, 
        project=st.session_state[f"{PAGE}.project_ds"], 
        filters=st.session_state[f"{PAGE}.filters_ds"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
