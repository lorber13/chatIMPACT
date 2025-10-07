import streamlit as st


conceptual_map_image = """
<img src="./app/static/ER_simplified_final_zoomed.png" alt="DB Model" width="700" height="289">
"""
# SINISTRA, SU , DESTRA, GIU

image_1 = """
<img src="./app/static/1.png" alt="query_1" usemap="#image-map" width="1000" height="200">
"""

title_alignment = """
<h1 style='text-align: center; color: Blue;'>A conceptual map for exploring the landscape of Large Language Models</h1>
"""

st.html(title_alignment)
st.html(conceptual_map_image)

st.markdown("---")

# Insert clickable image that redirects to different pages, ones for each entity

# st.markdown(image_1, unsafe_allow_html=True)

st.markdown("### A quick guide")
intro = """
As a Proof of Concept, it is possible to test the queries described in the paper **"A conceptual map for exploring the landscape of Large Language Models"**. This supports users in understanding how a tool based on the proposed conceptual map can answer meaningful questions.  
"""
st.markdown(intro)
# add some space
st.markdown("")
st.markdown("---")
st.markdown("")
# Add image for Query 1
st.markdown('<img src="./app/static/1.png" alt="Query 1" width="1000" height="200">', unsafe_allow_html=True)
query_1_desc = """
**Query 1:** *“Find the open-source Italian models with less than 8B parameters fine-tuned on the medical domain.”*  
This query considers the **trained_on** relationship between the **Model** and **Dataset** entities.  
"""
st.markdown(query_1_desc)

# Add button for pre-configured Query 1
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Run Query 1**", key="medical_italian_query_button", use_container_width=True):
        st.switch_page("pages/medical_italian_query.py")

st.markdown("")
st.markdown("---")
st.markdown("")
# Add image for Query 2
st.markdown('<img src="./app/static/2.png" alt="Query 2" width="1000" height="200">', unsafe_allow_html=True)
query_2_desc = """
**Query 2:** *“Find the open-source models specialized in Financial Document Analysis with less than 8B parameters.”*  
This query considers the **suited_for** relationship between the **Model** and **Task** entities.  
"""
st.markdown(query_2_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Run Query 2**", key="financial_query_button", use_container_width=True):
        st.switch_page("pages/financial_query.py")


st.markdown("")
st.markdown("---")
st.markdown("")
# Add image for Query 3
st.markdown('<img src="./app/static/3.png" alt="Query 3" width="1000" height="200">', unsafe_allow_html=True)
query_3_desc = """
**Query 3:** *“Find datasets to train models for text summarization in legal domains, with docs in English, Italian, Spanish, German, and French.”*  
This query uses the **enabled_by** relationship between **Dataset** and **Task**.   
"""
st.markdown(query_3_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Run Query 3**", key="legal_query_button", use_container_width=True):
        st.switch_page("pages/legal_query.py")



st.markdown("")
st.markdown("---")
st.markdown("")
# Add image for Query 4
st.markdown('<img src="./app/static/4.png" alt="Query 4" width="1000" height="200">', unsafe_allow_html=True)
query_4_desc = """
**Query 4:** *“Find Apache2.0 models trained on at least a dataset from mathematics, chemistry, and physics.”*  
This query considers the **trained_on** relationship between **Model** and **Dataset**.  
"""
st.markdown(query_4_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Run Query 4**", key="science_query_button", use_container_width=True):
        st.switch_page("pages/science_query.py")

st.markdown("")
st.markdown("---")
st.markdown("")
# Add image for Query 5
st.markdown('<img src="./app/static/5.png" alt="Query 5" width="1000" height="200">', unsafe_allow_html=True)
query_5_desc = """
**Query 5:** *“Find models with more than 70B parameters trained on English datasets, ranked by lowest carbon emissions.”*  
This query uses the **trained_on** relationship between **Model** and **Dataset**.  
"""
st.markdown(query_5_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Run Query 5**", key="large_models_query_button", use_container_width=True):
        st.switch_page("pages/large_models_query.py")

st.markdown("")
st.markdown("---")
st.markdown("")
# Add image for Query 6
st.markdown('<img src="./app/static/6.png" alt="Query 6" width="1000" height="200">', unsafe_allow_html=True)
query_6_desc = """
**Query 6:** *"Find instruction-tuned models under 8B parameters for code generation, ranked by a suitable metric."*  
This query connects **Model**s to **Task**s through the **suited_for** relationship and **Metric**s to **Model**s through the **evaluates** relationship."""
st.markdown(query_6_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Run Query 6**", key="code_generation_query_button", use_container_width=True):
        st.switch_page("pages/code_generation_query.py")

st.markdown("---")

# About section
st.markdown("## 📖 Documentation")
about_desc = """
Learn more about the **JSON-LD schema** that powers this tool's backend.
"""
st.markdown(about_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**📋 About - JSON-LD Schema**", key="about_button", use_container_width=True):
        st.switch_page("pages/about.py")

st.markdown("---")
