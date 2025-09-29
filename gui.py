import streamlit as st

# query = [
#     {
#         "collection": "Models",
#         "project": [
#             "name",
#             "openSource"
#         ],
#         "filters": {
#             "name": "ll", "openSource": True
#         }
#     },
#     {
#         "collection", "Downstream Tasks",
#         "project": [
#             "name",
#         ],
#         "filters": {
#             "name": "RO"
#         }
#     }
# ]
#
# result = [
#     {
#         "collection1": {
#             "attribute1": "examplevalue",
#             "attribute2": 3,
#         },
#         "collection2": {
#             "attribute1": [
#                 "value1",
#                 "value2",
#             ],
#         },
#     },
#     {
#         "collection1": {
#             "attribute1": "examplevalue2",
#             "attribute2": 5,
#         },
#         "collection2": {
#             "attribute1": [
#                 "value3",
#                 "value4",
#             ],
#         },
#     }
# ]

interactive_image_html = """
<img src="./app/static/ER_simplified_final_zoomed.png" alt="DB Model" usemap="#image-map" width="700" height="289">

<map name="image-map">                       
    <area target="" alt="Large Language Model" title="Model" href="llm_query" coords="280,15,420,95" shape="rect">
    <area target="" alt="Metric" title="Metric" href="metric_query" coords="0,210,150,290" shape="rect">
    <area target="" alt="Downstream Task" title="Task" href="downstream_task_query" coords="270,210,415,290" shape="rect">
    <area target="" alt="Dataset" title="Dataset" href="dataset_query" coords="550,210,700,290" shape="rect">
    <area target="" alt="Assess" title="Assesses" href="assess_query" coords="170,240,260,280" shape="rect">
    <area target="" alt="Evaluate" title="Evaluates" href="evaluate_query" coords="160,115,260,180" shape="rect">
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

st.markdown(image_1, unsafe_allow_html=True)

st.markdown("### A quick guide")
intro = """
To test this Proof of Concept, it is useful to refer to some example queries.  
The following queries will help the user understand how to navigate the interface and
why the tool is able to answer meaningful questions.  
"""
st.markdown(intro)

query_1_desc = """
**Query 1:** *“Find the open source models with less than 8 billion parameters, fine-tuned on the medical domain.”*  
The query considers the Train relationship between the **LargeLanguageModel** and **Dataset** entities.  
Click on the **Train** relationship to proceed.
"""
st.markdown(query_1_desc)

query_2_desc =  """
**Query 2**: *“Find an untrained metric with character-based granularity suitable for machine translation.”*  
This query considers the **Assess** relationship between the **Metric** and **DownstreamTask** entities.  
Click on the **Assess** relationship to proceed.
"""
st.markdown(query_2_desc)

query_3_desc = """
**Query 3**: *“Find open-source Large Language Models that are specialized in Code Generation with at least 4k context length.”*  
The query takes into account the **SuitedFor** relationship between the **LargeLanguageModel** and **DownstreamTask** entities.  
Click on the **SuitedFor** relationship.
"""
st.markdown(query_3_desc)

query_4_desc = """
**Query 4**: *"Find the datasets that can be used to train a model for text summarization and belong to the legal domain. Moreover, the datasets should contain documents written in English, Italian, Spanish, German and French."*  
The query takes into account the **Enable** relationship between the **Dataset** and **DownstreamTask** entities.  
Click on the **Enable** relationship.
"""
st.markdown(query_4_desc)

query_5_desc = """
**Query 5**: *"Find metrics that evaluate code generation models, focusing on open-source models with specific parameter counts."*  
This query considers the **Evaluate** relationship between the **Metric** and **LargeLanguageModel** entities.  
Click on the **Evaluate** relationship to proceed.
"""
st.markdown(query_5_desc)