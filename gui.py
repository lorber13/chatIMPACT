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
<img src="./app/static/ER_simplified_final_zoomed.png" alt="DB Model" usemap="#image-map" width="950" height="392">

<map name="image-map">
    <area target="" alt="Large Language Model" title="Large Language Model" href="llm_query" coords="392,249,553,294" shape="rect">
    <area target="" alt="Metric" title="Metric" href="metric_query" coords="76,255,150,288" shape="rect">
    <area target="" alt="Downstream Task" title="Downstream Task" href="downstream_task_query" coords="409,45,535,87" shape="rect">
    <area target="" alt="Dataset" title="Dataset" href="dataset_query" coords="805,254,876,289" shape="rect">
    <area target="" alt="Assess" title="Assess" href="assess_query" coords="113,125,138,148,113,172,89,150" shape="poly">
    <!-- <area target="" alt="Evaluate" title="Evaluate" href="link6" coords="276,248,302,272,277,295,252,273" shape="poly"> -->
    <area target="" alt="Train" title="Train" href="train_query" coords="649,248,672,272,650,297,625,272" shape="poly">
    <area target="" alt="Enable" title="Enable" href="enable_query" coords="840,125,865,150,841,174,818,149" shape="poly">
    <area target="" alt="Suited For" title="Suited For" href="suited_for_query" coords="473,110,497,136,472,158,449,135" shape="poly">
</map>
"""

title_alignment = """
<h1 style='text-align: center; color: Black;'>Chat IMPACT Knowledge Graph</h1>
"""

st.html(title_alignment)
st.html(interactive_image_html)

st.markdown("---")

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
**Query 4**: *“Find the datasets that can be used to train a model for text summarization and belong to the legal domain. Moreover, the datasets should contain documents written in English, Italian, Spanish, German and French."*  
The query takes into account the **Enable** relationship between the **Dataset** and **DownstreamTask** entities.  
Click on the **Enable** relationship.
"""
st.markdown(query_4_desc)