import streamlit as st


interactive_image_html = """
<img src="./app/static/ER_simplified_final_zoomed.png" alt="DB Model" usemap="#image-map" width="700" height="289">

<map name="image-map">                       
    <area target="" alt="Large Language Model" title="Model" href="llm_query" coords="280,15,420,95" shape="rect">
    <area target="" alt="Metric" title="Metric" href="metric_query" coords="0,210,150,290" shape="rect">
    <area target="" alt="Downstream Task" title="Task" href="downstream_task_query" coords="270,210,415,290" shape="rect">
    <area target="" alt="Dataset" title="Dataset" href="dataset_query" coords="550,210,700,290" shape="rect">
    <area target="" alt="Assess" title="Assesses" href="assess_query" coords="170,240,260,280" shape="rect">
    <area target="" alt="Evaluate" title="Evaluates" href="link6" coords="160,115,260,180" shape="rect">
    <area target="" alt="Train" title="Trained on" href="train_query" coords="420,120,500,200" shape="rect">
    <area target="" alt="Test" title="Tested on" href="test_query" coords="490,110,590,190" shape="rect">
    <area target="" alt="Enable" title="Enabled by" href="enable_query" coords="425,240,540,280" shape="rect">
    <area target="" alt="Suited For" title="Suited For" href="suited_for_query" coords="300,110,370,200" shape="rect">
</map>
"""
# SINISTRA, SU , DESTRA, GIU

image_1 = """
<img src="./app/static/1.png" alt="query_1" usemap="#image-map" width="1000" height="200">
"""

title_alignment = """
<h1 style='text-align: center; color: Blue;'>A conceptual map for exploring the landscape of Large Language Models</h1>
"""

st.html(title_alignment)
st.html(interactive_image_html)

st.markdown("---")

# Insert clickable image that redirects to different pages, ones for each entity

# st.markdown(image_1, unsafe_allow_html=True)

st.markdown("### A quick guide")
intro = """
To test this Proof of Concept, it is useful to refer to some example queries.  
The following queries will help the user understand how to navigate the interface and
why the tool is able to answer meaningful questions.  
"""
st.markdown(intro)
# add some space
st.markdown("")
st.markdown("")
# Add image for Query 1
st.markdown('<img src="./app/static/1.png" alt="Query 1" width="1000" height="200">', unsafe_allow_html=True)
query_1_desc = """
**Query 1:** *“Find the open-source Italian models with less than 8B parameters fine-tuned on the medical domain.”*  
This query considers the **Train** relationship between the **Model** and **Dataset** entities.  
"""
st.markdown(query_1_desc)

# Add button for pre-configured Query 1
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 **Run Query 1 (Pre-configured)**", key="medical_italian_query_button", use_container_width=True):
        st.switch_page("pages/medical_italian_query.py")

st.markdown("")
st.markdown("")
# Add image for Query 2
st.markdown('<img src="./app/static/2.png" alt="Query 2" width="1000" height="200">', unsafe_allow_html=True)
query_2_desc = """
**Query 2:** *“Find the open-source models specialized in Financial Document Analysis with less than 8B parameters.”*  
This query considers the **SuitedFor** relationship between the **Model** and **Task** entities.  
Click on the **SuitedFor** edge and apply:  
- **Model filters:** OpenSource=True, NumberOfParameters < 8B  
- **Task filters:** SubTask = Financial Document Analysis  
"""
st.markdown(query_2_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 **Run Query 2 (Pre-configured)**", key="financial_query_button", use_container_width=True):
        st.switch_page("pages/financial_query.py")


st.markdown("")
st.markdown("")
# Add image for Query 3
st.markdown('<img src="./app/static/3.png" alt="Query 3" width="1000" height="200">', unsafe_allow_html=True)
query_3_desc = """
**Query 3:** *“Find datasets to train models for text summarization in legal domains, with docs in English, Italian, Spanish, German, and French.”*  
This query uses the **Enable** relationship between **Dataset** and **Task**.  
Click on the **Enable** edge and apply:  
- **Task filters:** Downstream Task = Summarization  
- **Dataset filters:** Domain=Law, Language ∈ {English, Italian, Spanish, German, French}  
"""
st.markdown(query_3_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 **Run Query 3 (Pre-configured)**", key="legal_query_button", use_container_width=True):
        st.switch_page("pages/legal_query.py")



st.markdown("")
st.markdown("")
# Add image for Query 4
st.markdown('<img src="./app/static/4.png" alt="Query 4" width="1000" height="200">', unsafe_allow_html=True)
query_4_desc = """
**Query 4:** *“Find Apache2.0 models trained on at least a dataset from mathematics, chemistry, and physics.”*  
This query considers the **Train** relationship between **Model** and **Dataset**.  
Click on the **Train** edge and apply:  
- **Model filters:** LicenseToUse = Apache2.0  
- **Dataset filters:** Domain ∈ {Mathematics, Chemistry, Physics}  
"""
st.markdown(query_4_desc)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 **Run Query 4 (Pre-configured)**", key="science_query_button", use_container_width=True):
        st.switch_page("pages/science_query.py")

st.markdown("")
st.markdown("")
# Add image for Query 5
st.markdown('<img src="./app/static/5.png" alt="Query 5" width="1000" height="200">', unsafe_allow_html=True)
query_5_desc = """
**Query 5:** *“Find models with more than 70B parameters trained on English datasets, ranked by lowest carbon emissions.”*  
This query uses the **Train** relationship between **Model** and **Dataset**.  
Click on the **Train** edge and apply:  
- **Model filters:** NumberOfParameters > 70B  
- **Dataset filters:** Language = English  
- **Ranking options:** CarbonEmissions (ascending)  
"""
st.markdown(query_5_desc)

st.markdown("")
st.markdown("")
# Add image for Query 6
st.markdown('<img src="./app/static/6.png" alt="Query 6" width="1000" height="200">', unsafe_allow_html=True)
query_6_desc = """
**Query 6:** *“Find instruction-tuned models under 8B parameters for code generation, ranked by a suitable metric.”*  
This query considers the **Evaluate** relationship between **Metric**, **Model**, and **Task**.  
Click on the **triple query button** (Metric–Model–Task) and apply:  
- **Model filters:** InstructionTuned=True, NumberOfParameters < 8B  
- **Task filters:** SubTask = Code Generation  
- **Ranking options:** select a metric suitable for code generation (e.g., Tabby score)  
"""
st.markdown(query_6_desc)

st.markdown("")
st.markdown("")

# Add triple query button
st.markdown("### Triple Query (Model-Task-Metric)")
st.markdown("For complex queries involving relationships between Models, Tasks, and Metrics:")

if st.button("🔗 **Triple Query: Model-Task-Metric**", key="trio_query_button", use_container_width=True):
    st.switch_page("pages/trio_query.py")

st.markdown("---")