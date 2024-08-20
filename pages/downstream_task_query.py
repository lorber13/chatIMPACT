import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao


COLLECTION = "Downstream Tasks"

dao = Dao("ChatIMPACT")

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Downstream Task</h1>
"""

st.html(title_alignment)
st.image("static/downstream_task.png")

st.markdown("---")

filters = {}
project = st.multiselect(
    "**Select the results of the query**",
    dao.get_attributes("Downstream Tasks"),
    ["name"],
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
