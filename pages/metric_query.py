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
st.image("static/metrics.png", use_column_width=True)

st.markdown("---")
st.html("<h3 style='text-align: center;'>Metric filters</h3>")
col_1, col_2 = st.columns([1, 1])

with col_1:
    st.radio("**Context Free**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.contextFree")
    st.radio("**Trained**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.trained")
    st.radio("**Feature Based**", ["No filter", "True", "False"], index=0, key=f"{PAGE}.featureBased")

with col_2:
    if st.session_state[f"{PAGE}.trained"] == "True":
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

st.session_state[f"{PAGE}.filters"] = {}

# Add filters only if not "No filter"
if st.session_state[f"{PAGE}.trained"] != "No filter":
    st.session_state[f"{PAGE}.filters"]["trained"] = st.session_state[f"{PAGE}.trained"] == "True"
if st.session_state[f"{PAGE}.contextFree"] != "No filter":
    st.session_state[f"{PAGE}.filters"]["contextFree"] = st.session_state[f"{PAGE}.contextFree"] == "True"
if st.session_state[f"{PAGE}.featureBased"] != "No filter":
    st.session_state[f"{PAGE}.filters"]["featureBased"] = st.session_state[f"{PAGE}.featureBased"] == "True"

if st.session_state[f"{PAGE}.trained"] == "False":
    if st.session_state[f"{PAGE}.gran"]:
        st.session_state[f"{PAGE}.filters"]["granularity"] = {
            "$all": st.session_state[f"{PAGE}.gran"]
        }
if st.session_state[f"{PAGE}.trained"] == "True":
    if st.session_state[f"{PAGE}.feat"]:
        st.session_state[f"{PAGE}.filters"]["featureBased/endToEnd"] = {
            "$all": st.session_state[f"{PAGE}.feat"]
        }

st.multiselect(
    "**Select the results of the query**",
    dao.get_attributes(COLLECTION),
    ["name", "description"],
    key=f"{PAGE}.project_multiselect"
)
st.session_state[f"{PAGE}.project"] = st.session_state[f"{PAGE}.project_multiselect"]

with st.expander("**📊 Ranking Options**", expanded=False):
    st.info("Note: Metrics collection has no numeric fields suitable for ranking. Results will be displayed in default order. When ranking is activated on other pages, entries with null values for the ranking field are automatically excluded from results.")

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
