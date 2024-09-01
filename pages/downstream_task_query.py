import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Downstream Task"
COLLECTION = "Downstream Tasks"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("static/downstream_task.svg")

st.markdown("---")

st.session_state[f"{PAGE}.filters"] = {}
st.multiselect(
    "**Select the results of the query from Downstream Task**",
    dao.get_attributes(COLLECTION),
    ["name"],
    key=f"{PAGE}.project_dt_multiselect"
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = [create_query_structure(
        collection=COLLECTION, 
        project=st.session_state[f"{PAGE}.project_dt_multiselect"],
        filters=st.session_state[f"{PAGE}.filters"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)
