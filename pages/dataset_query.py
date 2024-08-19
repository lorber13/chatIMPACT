import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao


COLLECTION = "Datasets"

dao = Dao("Paper")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Dataset</h1>
"""

st.html(title_alignment)
st.image("static/dataset.png")

st.markdown("---")
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
    training = st.toggle("**Training Dataset**", value=None)
    fine_tuning = st.toggle("**Fine-Tuning Dataset**", value=None)
    evaluation = st.toggle("**Evaluation Dataset**", value=None)
    domain = st.multiselect(
        "**Domain**",
        dao.get_all("Datasets", "domain"),
        ["Miscellaneous"]
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
    lan = st.multiselect(
        "**Language**",
        dao.get_all("Datasets", "languages"),
        ["English"],
    )
    lic = st.multiselect(
        "**LicenseToUse**",
        dao.get_all("Datasets", "licenseToUse"),
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

filters = { 
    # "contextLength": {"$gte": cont_length},
}

if type_filter == "Disk space (GB)":
    filters["$and"] = [
        {"size [GB]": {"$gte": min_size_gb}},
        {
            "size [GB]": {"$lte": max_size_gb if max_size_gb else 1e9}
        },  # TODO: numero
    ]

if type_filter == "Row count":
    filters["$and"] = [
        {"size [rows]": {"$gte": min_size_rows}},
        {
            "size [rows]": {"$lte": max_size_rows if max_size_rows else 1e9}
        },  # TODO: numero
    ]

if training:
    filters["trainingDataset"] = training

if fine_tuning:
    filters["fineTuning"] = fine_tuning

if evaluation:
    filters["evaluationDataset"] = evaluation

if domain:
    filters["domain"] = {"$all": domain}

if lic:
    filters["licenseToUse"] = {"$all": lic}

if lan:
    filters["languages"] = {"$all": lan}

project = st.multiselect(
    "**Select the results of the query**",
    [
        "name",
        "size [GB]",
        "size [rows]",
        "languages",
        "licenseToUse",
        "domain",
        "uri",
        "trainingDataset",
        "fineTuning",
        "evaluationDataset",
    ],
    ["name", "uri", "domain"],
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=COLLECTION, project=project, filters=filters
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
