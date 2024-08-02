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
<img src="./app/static/db_model.jpeg" alt="DB Model" usemap="#image-map">

<map name="image-map">
    <area target="" alt="Large Language Model" title="Large Language Model" href="http://localhost:8501/llm_query" coords="392,249,553,294" shape="rect">
    <area target="" alt="Metric" title="Metric" href="link2" coords="76,255,150,288" shape="rect">
    <area target="" alt="Downstream Task" title="Downstream Task" href="link3" coords="409,45,535,87" shape="rect">
    <area target="" alt="Dataset" title="Dataset" href="link4" coords="805,254,876,289" shape="rect">
    <area target="" alt="Assess" title="Assess" href="link5" coords="113,125,138,148,113,172,89,150" shape="poly">
    <area target="" alt="Evaluate" title="Evaluate" href="link6" coords="276,248,302,272,277,295,252,273" shape="poly">
    <area target="" alt="Train" title="Train" href="Link7" coords="649,248,672,272,650,297,625,272" shape="poly">
    <area target="" alt="Enable" title="Enable" href="Link8" coords="840,125,865,150,841,174,818,149" shape="poly">
    <area target="" alt="Suited For" title="Suited For" href="Link9" coords="473,110,497,136,472,158,449,135" shape="poly">
</map>
"""

title_alignment = """
<h1 style='text-align: center; color: Black;'>Chat IMPACT Knowledge Graph</h1>
"""

st.html(title_alignment)
st.html(interactive_image_html)

