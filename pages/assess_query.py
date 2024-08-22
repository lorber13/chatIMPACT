import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Assess"
METRICS = "Metrics"
DOWNSTREAM_TASKS = "Downstream Tasks"

dao = Dao("ChatIMPACT")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Assess</h1>
"""

st.html(title_alignment)
st.image("static/assess.svg")

### SECTION FOR METRICS ###

st.markdown("---")
st.html("<h3 style='text-align: center;'>Metrics filters</h3>")
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
    st.multiselect(
        "**Context**",
        dao.get_all(METRICS, "context"),
        key=f"{PAGE}.context",
        default=st.session_state[f"{PAGE}.context"] if f"{PAGE}.context" in st.session_state else None
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
    st.toggle("**Trained**",
              value=False,
              key=f"{PAGE}.trained")

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
    if st.session_state[f"{PAGE}.trained"]:
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

st.session_state[f"{PAGE}.filters_metrics"] = {
    f"{METRICS}.trained": st.session_state[f"{PAGE}.trained"]
}

if st.session_state[f"{PAGE}.context"]:
    st.session_state[f"{PAGE}.filters_metrics"][f"{METRICS}.context"] = {
        "$all": st.session_state[f"{PAGE}.context"]
    }

if not st.session_state[f"{PAGE}.trained"]:
    if st.session_state[f"{PAGE}.gran"]:
        st.session_state[f"{PAGE}.filters_metrics"][f"{METRICS}.granularity"] = {
            "$all": st.session_state[f"{PAGE}.gran"]
        }
if st.session_state[f"{PAGE}.trained"]:
    if st.session_state[f"{PAGE}.feat"]:
        st.session_state[f"{PAGE}.filters_metrics"][f"{METRICS}.featureBased/endToEnd"] = {
            "$all": st.session_state[f"{PAGE}.feat"]
        }

### SECTION FOR DOWNSTREAM TASKS ###
st.markdown("---")
st.html(f"<h3 style='text-align: center;'>{DOWNSTREAM_TASKS} filters</h3>")
st.multiselect(
    "**Downstream Task name**",
    dao.get_all("Downstream Tasks", "name"),
    key=f"{PAGE}.name_dt",
    default=st.session_state[f"{PAGE}.name_dt"] if f"{PAGE}.name_dt" in st.session_state else None
)
st.session_state[f"{PAGE}.filters_dt"] = {}

if st.session_state[f"{PAGE}.name_dt"]:
    st.session_state[f"{PAGE}.filters_dt"][f"{DOWNSTREAM_TASKS}.name"] = st.session_state[f"{PAGE}.name_dt"][0]

### FINAL SECTION FOR QUERYING
st.markdown("---")
st.multiselect(
    "**Select the results of the query for Metrics**",
    dao.get_attributes(METRICS),
    ["name", "description "],
    key=f"{PAGE}.project_metrics_multiselect"
)
st.session_state[f"{PAGE}.project_metrics"] = [
    f"{METRICS}." + att for att in st.session_state[f"{PAGE}.project_metrics_multiselect"]]

st.multiselect(
    "**Select the results of the query from Downstream Task**",
    dao.get_attributes(DOWNSTREAM_TASKS),
    ["name"],
    key=f"{PAGE}.project_dt_multiselect"
)
st.session_state[f"{PAGE}.project_dt"] = [
    f"{DOWNSTREAM_TASKS}." + att for att in st.session_state[f"{PAGE}.project_dt_multiselect"]]

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=METRICS, 
        project=st.session_state[f"{PAGE}.project_metrics"], 
        filters=st.session_state[f"{PAGE}.filters_metrics"]
    ),
    create_query_structure(
        collection=DOWNSTREAM_TASKS,
        project=st.session_state[f"{PAGE}.project_dt"],
        filters=st.session_state[f"{PAGE}.filters_dt"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
