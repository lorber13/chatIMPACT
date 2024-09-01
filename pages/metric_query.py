import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Metric"
COLLECTION = "Metrics"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("static/metrics.svg")

st.markdown("---")
st.html("<h3 style='text-align: center;'>Metric filters</h3>")
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
        dao.get_all(COLLECTION, "context"),
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
            dao.get_all(COLLECTION, "featureBased/endToEnd"),
            key=f"{PAGE}.feat",
            default=st.session_state[f"{PAGE}.feat"] if f"{PAGE}.feat" in st.session_state else None
        )
    else:
        st.multiselect(
            "**Granularity**",
            dao.get_all(COLLECTION, "granularity"),
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

st.session_state[f"{PAGE}.filters"] = {
    "trained": st.session_state[f"{PAGE}.trained"]
}

if st.session_state[f"{PAGE}.context"]:
    st.session_state[f"{PAGE}.filters"]["context"] = {
        "$all": st.session_state[f"{PAGE}.context"]
    }

if not st.session_state[f"{PAGE}.trained"]:
    if st.session_state[f"{PAGE}.gran"]:
        st.session_state[f"{PAGE}.filters"]["granularity"] = {
            "$all": st.session_state[f"{PAGE}.gran"]
        }
if st.session_state[f"{PAGE}.trained"]:
    if st.session_state[f"{PAGE}.feat"]:
        st.session_state[f"{PAGE}.filters"]["featureBased/endToEnd"] = {
            "$all": st.session_state[f"{PAGE}.feat"]
        }

st.multiselect(
    "**Select the results of the query**",
    dao.get_attributes(COLLECTION),
    ["name", "description "],
    key=f"{PAGE}.project_multiselect"
)
st.session_state[f"{PAGE}.project"] = st.session_state[f"{PAGE}.project_multiselect"]

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=COLLECTION, 
        project=st.session_state[f"{PAGE}.project"],
        filters=st.session_state[f"{PAGE}.filters"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
