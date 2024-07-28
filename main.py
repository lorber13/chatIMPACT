import streamlit as st

from database import db

models = db["Models"].find()

st.write("""
# Database
## Models
""")

st.json([*models])
