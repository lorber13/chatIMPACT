import streamlit as st
from utils import create_query_structure
from dao import Dao


COLLECTION = "Models"

dao = Dao("Paper")

title_alignment = """
<h1 style='text-align: center; color: Black;'>Large Language Model</h1>
"""

st.html(title_alignment)
st.image("static/llm.png")

st.markdown("---")
col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
)

with col_1:
    st.html(
        """
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            """
    )

with col_2:
    min_num_param = st.number_input(
        "**Minimum number of parameters**", min_value=0, value=0
    )
    max_num_param = st.number_input(
        "**Maximum number of parameters**", min_value=0, value=None
    )

with col_3:
    st.html(
        """
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            """
    )

with col_4:
    open_source = st.toggle("**Open Source**", value=False)
    fine_tuned = st.toggle("**Fine-Tuned**", value=False)
    quantization = st.toggle("**Quantization**", value=False)
    cont_length = st.number_input(
        "**Minimum context length**",
        min_value=0,
    )

with col_5:
    st.html(
        """
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        """
    )

with col_6:
    lan = st.multiselect(
        "**Language**",
        [
            "English",
            "Italian",
            "Spanish",
            "French",
            "Portuguese",
            "German",
            "Multilingual",
        ],
        ["English"],
    )
    arch = st.multiselect(
        "**Architecture**",
        ["LLaMA"],
    )

with col_7:
    st.html(
        """
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        """
    )

filters = {
    "$and": [
        {"numberOfParameters [B]": {"$gte": min_num_param}},
        {
            "numberOfParameters [B]": {"$lte": max_num_param if max_num_param else 1e9}
        },  # TODO: numero
    ],
    "openSource": open_source,
    "fineTuned": fine_tuned,
    # "quantization": quantization,  # FIXME: fixami
    # "contextLength": {"$gte": cont_length},
}

if arch:
    filters["architecture"] = arch[0]

if lan:
    filters["languages"] = {"$all": lan}

project = st.multiselect(
    "**Select the results of the query**",
    [
        "name",
        "version",
        "numberOfParameters [B]",
        "quantization",
        "architecture",
        "languages",
        "modelCreator",
        "licenseToUse",
        "libraryFramework",
        "contextLength",
        "developers",
        "openSource",
        "uri",
        "fineTuned",
        "carbonEmission [CO2eq tons]",
        "tokenizer",
    ],
    ["name", "version", "numberOfParameters [B]"],
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    query_input = create_query_structure(
        collection=COLLECTION, project=project, filters=filters
    )
    st.write(query_input)
    result = dao.query([query_input])
    st.write(result)
