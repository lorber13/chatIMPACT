import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao


DOWNSTREAM_TASKS = "Downstream Tasks"
DATASETS = "Datasets"

dao = Dao("ChatIMPACT")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Train</h1>
"""

st.html(title_alignment)
st.image("static/enable.png")

### SECTION FOR DOWNSTREAM TASKS ###

filters_dt = {}

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
    type_filter = st.radio(
    "***Filter on Dataset size***",
    ["No filters", "Disk space (GB)", "Row count"],
    )
    if type_filter == "Disk space (GB)":
        min_size_gb = st.number_input(
            "**Minimum size [GB]**", min_value=0, value=0
        )
        max_size_gb = st.number_input(
            "**Maximum size [GB]**", min_value=0, value=None
        )
    if type_filter == "Row count":
        min_size_rows = st.number_input(
            "**Minimum size [rows]**", min_value=0, value=0
        )
        max_size_rows = st.number_input(
            "**Maximum size [rows]**", min_value=0, value=None
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
    training = st.toggle("**Training Dataset**", value=None)
    fine_tuning = st.toggle("**Fine-Tuning Dataset**", value=None)
    evaluation = st.toggle("**Evaluation Dataset**", value=None)
    domain = st.multiselect(
        "**Domain**",
        dao.get_all("Datasets", "domain")
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
    lan_ds = st.multiselect(
        "**Language**",
        dao.get_all("Datasets", "languages"),
    )
    lic = st.multiselect(
        "**LicenseToUse**",
        dao.get_all("Datasets", "licenseToUse"),
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

filters_ds = { 
    # "contextLength": {"$gte": cont_length},
}

if type_filter == "Disk space (GB)":
    filters_ds["$and"] = [
        {f"{DATASETS}.size [GB]": {"$gte": min_size_gb}},
        {
            f"{DATASETS}.size [GB]": {"$lte": max_size_gb if max_size_gb else 1e9}
        },  # TODO: numero
    ]

if type_filter == "Row count":
    filters_ds["$and"] = [
        {f"{DATASETS}.size [rows]": {"$gte": min_size_rows}},
        {
            f"{DATASETS}.size [rows]": {"$lte": max_size_rows if max_size_rows else 1e9}
        },  # TODO: numero
    ]

if training:
    filters_ds[f"{DATASETS}.trainingDataset"] = training

if fine_tuning:
    filters_ds[f"{DATASETS}.fineTuning"] = fine_tuning

if evaluation:
    filters_ds[f"{DATASETS}.evaluationDataset"] = evaluation

if domain:
    filters_ds[f"{DATASETS}.domain"] = {"$all": domain}

if lic:
    filters_ds[f"{DATASETS}.licenseToUse"] = {"$all": lic}

if lan_ds:
    filters_ds[f"{DATASETS}.languages"] = {"$all": lan_ds}

### FINAL SECTION FOR QUERYING
att_dt = [f"{DOWNSTREAM_TASKS}." + att for att in dao.get_attributes(DOWNSTREAM_TASKS)]
project_dt = st.multiselect(
    "**Select the results of the query from Downstream Task**",
    att_dt,
    [f"{DOWNSTREAM_TASKS}.name"],
)

att_ds = [f"{DATASETS}." + att for att in dao.get_attributes(DATASETS)]
project_ds = st.multiselect(
    "**Select the results of the query from Dataset**",
    att_ds,
    [f"{DATASETS}.name", f"{DATASETS}.uri", f"{DATASETS}.domain"],
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=DOWNSTREAM_TASKS, project=project_dt, filters=filters_dt
    ),
    create_query_structure(
        collection=DATASETS, project=project_ds, filters=filters_ds
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
