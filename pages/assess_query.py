import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao


METRICS = "Metrics"
DOWNSTREAM_TASKS = "Downstream Tasks"

dao = Dao("ChatIMPACT")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Assess</h1>
"""

st.html(title_alignment)
st.image("static/assess.png")

### SECTION FOR METRICS ###

st.markdown("---")
st.html("<h2 style='text-align: center;'>Metrics filters</h2>")
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
        dao.get_all(METRICS, "context")
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
            dao.get_all(METRICS, "featureBased/endToEnd")
        )
        granularity = None
    else:
        granularity = st.multiselect(
            "**Granularity**",
            dao.get_all(METRICS, "granularity")
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

filters_metrics = {
}

if context:
    filters_metrics[f"{METRICS}.context"] = {"$all": context}

if granularity:
    filters_metrics[f"{METRICS}.granularity"] = {"$all": granularity}

if feat:
    filters_metrics[f"{METRICS}.featureBased/endToEnd"] = {"$all": feat}

### SECTION FOR DOWNSTREAM TASKS ###
filters_dt = {}

### FINAL SECTION FOR QUERYING
att_metrics = [f"{METRICS}." + att for att in dao.get_attributes(METRICS)]
project_metrics = st.multiselect(
    "**Select the results of the query from Metrics**",
    att_metrics,
    [f"{METRICS}.name"],
)

att_dt = [f"{DOWNSTREAM_TASKS}." + att for att in dao.get_attributes(DOWNSTREAM_TASKS)]
project_dt = st.multiselect(
    "**Select the results of the query from Downstream Tasks**",
    att_dt,
    [f"{DOWNSTREAM_TASKS}.name"],
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=METRICS, project=project_metrics, filters=filters_metrics
    ),
    create_query_structure(
        collection=DOWNSTREAM_TASKS, project=project_dt, filters=filters_dt
    )]
    st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
