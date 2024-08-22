import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Dataset"
COLLECTION = "Datasets"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
st.image("static/dataset.svg")

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
        {f"size [GB]": {"$gte": st.session_state[f"{PAGE}.min_size_gb"]}},
        {
            f"size [GB]": {"$lte": st.session_state[f"{PAGE}.max_size_gb"] if \
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
    st.session_state[f"{PAGE}.filters_ds"][f"fineTuning"] = st.session_state[f"{PAGE}.fine_tuning"]

if st.session_state[f"{PAGE}.domain"]:
    st.session_state[f"{PAGE}.filters_ds"][f"domain"] = {
        "$all": st.session_state[f"{PAGE}.domain"]
    }

if st.session_state[f"{PAGE}.lic"]:
    st.session_state[f"{PAGE}.filters_ds"][f"licenseToUse"] = {
        "$all": st.session_state[f"{PAGE}.lic"]
    }

if st.session_state[f"{PAGE}.lan_ds"]:
    st.session_state[f"{PAGE}.filters_ds"][f"languages"] = {
        "$all": st.session_state[f"{PAGE}.lan_ds"]
    }

st.multiselect(
    "**Select the results of the query from Dataset**",
    dao.get_attributes(COLLECTION),
    ["name", "uri", "domain"],
    key=f"{PAGE}.project_ds_multiselect"
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=COLLECTION, 
        project=st.session_state[f"{PAGE}.project_ds_multiselect"], 
        filters=st.session_state[f"{PAGE}.filters_ds"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
