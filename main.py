import streamlit as st
from database import getDatabase

db = getDatabase("Paper")

models = db["Models"].find()

st.write("""
# Database
## Models
""")

st.json([*models])
