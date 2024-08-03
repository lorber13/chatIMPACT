"""main entry point"""

import streamlit as st
from database import get_database

db = get_database("Paper")

models = db["Models"].find()

st.write(
    """
# Database
## Models
"""
)

st.json([*models])
