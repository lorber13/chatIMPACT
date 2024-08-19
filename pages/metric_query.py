import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao


COLLECTION = "Evaluation Techniques"

dao = Dao("Paper")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Metric</h1>
"""

st.html(title_alignment)
st.image("static/metric.png")

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
    context = st.multiselect(
        "**Context**",
        dao.get_all("Evaluation Techniques", "context")
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
    trained = st.toggle("**Trained**", value=False)

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
    if trained:
        feat = st.multiselect(
            "**Feature Based - End to End**",
            dao.get_all("Evaluation Techniques", "featureBased/endToEnd")
        )
        granularity = None
    else:
        granularity = st.multiselect(
            "**Granularity**",
            dao.get_all("Evaluation Techniques", "granularity")
        )
        feat = None

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
    "trained": trained
}

if context:
    filters["context"] = {"$all": context}

if granularity:
    filters["granularity"] = {"$all": granularity}

if feat:
    filters["featureBased/endToEnd"] = {"$all": feat}

project = st.multiselect(
    "**Select the results of the query**",
    [
        "name",
        "description",
        "context",
        "trained",
        "featureBased/endToEnd",
        "granularity",
        "uri",
        "extra",
        "type"
    ],
    ["name", "uri", "description"],
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
