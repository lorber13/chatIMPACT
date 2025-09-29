import streamlit as st
import pandas as pd
from utils import create_query_structure, reworked_query_output
from dao import Dao

PAGE = "Dataset"
COLLECTION = "Datasets"
DB_NAME = "ChatIMPACT"

dao = Dao(DB_NAME)

st.page_link("gui.py", label="Homepage", icon="🏠")

title_alignment = f"<h1 style='text-align: center; color: Black;'>{PAGE}</h1>"

st.html(title_alignment)
st.image("static/dataset.png", use_column_width=True)

st.markdown("---")
st.html("<h3 style='text-align: center;'>Dataset filters</h3>")
col_9, col_10, col_11, col_12, col_13, col_14, col_15, col_16 = st.columns(
    [0.2, 5.9, 0.2, 5.9, 0.2, 5.9, 0.2, 5.9]
)

with col_9:
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

with col_10:
    st.radio(
        "***Filter on Dataset size***",
        ["No filters", "Row count"],
        key=f"{PAGE}.type_filter"
    )
    if st.session_state[f"{PAGE}.type_filter"] == "Row count":
        st.number_input(
            "**Minimum size [rows]**", min_value=0, value=0,
            key=f"{PAGE}.min_size_rows"
        )
        st.number_input(
            "**Maximum size [rows]**", min_value=0, value=None,
            key=f"{PAGE}.max_size_rows"
        )

with col_11:
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

with col_12:
    st.radio("**Fine-Tuning Dataset**", 
             ["No filter", "True", "False"], 
             index=0,
             key=f"{PAGE}.fine_tuning")
    st.multiselect(
        "**Domain**",
        dao.get_all("Datasets", "domain"),
        key=f"{PAGE}.domain",
        default=st.session_state[f"{PAGE}.domain"] if f"{PAGE}.domain" in st.session_state else None
    )

with col_13:
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

with col_14:
    st.multiselect(
        "**Language**",
        dao.get_all("Datasets", "languages"),
        key=f"{PAGE}.lan_ds",
        default=st.session_state[f"{PAGE}.lan_ds"] if f"{PAGE}.lan_ds" in st.session_state else None
    )
    st.multiselect(
        "**LicenseToUse**",
        dao.get_all("Datasets", "licenseToUse"),
        key=f"{PAGE}.lic",
        default=st.session_state[f"{PAGE}.lic"] if f"{PAGE}.lic" in st.session_state else None
    )

with col_15:
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

st.session_state[f"{PAGE}.filters_ds"] = {}
st.session_state[f"{PAGE}.size_filter_active"] = False

if st.session_state[f"{PAGE}.type_filter"] == "Row count":
    # Convert string sizes to numeric values for comparison
    def convert_size_to_numeric(size_str):
        """Convert size strings like '194k', '2M' to numeric values"""
        if not size_str or size_str == "n/a":
            return 0
        size_str = size_str.lower()
        if size_str.endswith('k'):
            return float(size_str[:-1]) * 1000
        elif size_str.endswith('m'):
            return float(size_str[:-1]) * 1000000
        else:
            try:
                return float(size_str)
            except:
                return 0
    
    # Create a filter that works with string-based sizes
    min_rows = st.session_state[f"{PAGE}.min_size_rows"]
    max_rows = st.session_state[f"{PAGE}.max_size_rows"] if st.session_state[f"{PAGE}.max_size_rows"] else 1e9
    
    # We'll need to handle this filtering in the application layer since MongoDB
    # can't directly compare these string formats numerically
    st.session_state[f"{PAGE}.size_filter_active"] = True
    st.session_state[f"{PAGE}.min_rows"] = min_rows
    st.session_state[f"{PAGE}.max_rows"] = max_rows

if st.session_state[f"{PAGE}.fine_tuning"] != "No filter":
    st.session_state[f"{PAGE}.filters_ds"][f"fineTuning"] = st.session_state[f"{PAGE}.fine_tuning"] == "True"

if st.session_state[f"{PAGE}.domain"]:
    st.session_state[f"{PAGE}.filters_ds"][f"domain"] = {
        "$all": st.session_state[f"{PAGE}.domain"]
    }

if st.session_state[f"{PAGE}.lic"]:
    st.session_state[f"{PAGE}.filters_ds"][f"licenseToUse"] = {
        "$all": st.session_state[f"{PAGE}.lic"]
    }

if st.session_state[f"{PAGE}.lan_ds"]:
    st.session_state[f"{PAGE}.filters_ds"][f"languages"] = {
        "$all": st.session_state[f"{PAGE}.lan_ds"]
    }

st.multiselect(
    "**Select the results of the query from Dataset**",
    dao.get_attributes(COLLECTION),
    ["name", "uri", "domain"],
    key=f"{PAGE}.project_ds_multiselect"
)

l, l1, c, r1, r = st.columns(5)

with c:
    query = st.button("Get results")

if query:
    # Ensure 'size' is included in projection if size filtering is active
    project_fields = st.session_state[f"{PAGE}.project_ds_multiselect"].copy()
    if st.session_state.get(f"{PAGE}.size_filter_active", False) and "size" not in project_fields:
        project_fields.append("size")
    
    # Add ranking fields to project if ranking is active
    if st.session_state[f"{PAGE}.rank_by"] == "Dataset Size" and "size" not in project_fields:
        project_fields.append("size")
    
    query_input = [create_query_structure(
        collection=COLLECTION, 
        project=project_fields, 
        filters=st.session_state[f"{PAGE}.filters_ds"]
    )]
    #st.write(query_input)
    result = dao.query(query_input)
    
    # Apply size filtering if active
    if st.session_state.get(f"{PAGE}.size_filter_active", False):
        def convert_size_to_numeric(size_str):
            """Convert size strings like '194k', '2M' to numeric values"""
            if not size_str or size_str == "n/a":
                return 0
            size_str = str(size_str).lower()
            if size_str.endswith('k'):
                return float(size_str[:-1]) * 1000
            elif size_str.endswith('m'):
                return float(size_str[:-1]) * 1000000
            else:
                try:
                    return float(size_str)
                except:
                    return 0
        
        min_rows = st.session_state[f"{PAGE}.min_rows"]
        max_rows = st.session_state[f"{PAGE}.max_rows"]
        
        # Filter results based on numeric size comparison
        filtered_result = []
        
        for item in result:
            # Access size from the correct nested structure
            size_value = None
            if 'Datasets' in item and 'size' in item['Datasets']:
                size_value = item['Datasets']['size']
            
            if size_value is not None:
                numeric_size = convert_size_to_numeric(size_value)
                if min_rows <= numeric_size <= max_rows:
                    filtered_result.append(item)
            elif min_rows == 0:  # Include items without size if min is 0
                filtered_result.append(item)
        
        result = filtered_result
    
    # Apply ranking if selected
    if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
        def convert_size_to_numeric(size_str):
            """Convert size strings like '273k', '2M' to numeric values"""
            if not size_str or size_str == "n/a":
                return None
            size_str = str(size_str).upper()
            if size_str.endswith('K'):
                try:
                    return float(size_str[:-1]) * 1000
                except ValueError:
                    return None
            elif size_str.endswith('M'):
                try:
                    return float(size_str[:-1]) * 1000000
                except ValueError:
                    return None
            else:
                try:
                    return float(size_str)
                except ValueError:
                    return None
        
        def has_valid_ranking_value(item):
            """Check if item has a valid (non-null) value for the selected ranking field"""
            if st.session_state[f"{PAGE}.rank_by"] == "Dataset Size":
                if 'Datasets' in item and 'size' in item['Datasets']:
                    return convert_size_to_numeric(item['Datasets']['size']) is not None
                return False
            return True
        
        def get_sort_key(item):
            if st.session_state[f"{PAGE}.rank_by"] == "Dataset Size":
                if 'Datasets' in item and 'size' in item['Datasets']:
                    return convert_size_to_numeric(item['Datasets']['size']) or 0
                return 0
            return 0
        
        # Filter out items with null/missing ranking values
        result = [item for item in result if has_valid_ranking_value(item)]
        
        # Sort the remaining items
        reverse_order = st.session_state[f"{PAGE}.sort_order"] == "Descending (High to Low)"
        result = sorted(result, key=get_sort_key, reverse=reverse_order)
    
    df = pd.DataFrame(reworked_query_output(result))
    st.dataframe(df)

with st.expander("**📊 Ranking Options**", expanded=False):
    st.radio(
        "**Rank by**",
        ["No ranking", "Dataset Size"],
        index=0,
        key=f"{PAGE}.rank_by"
    )
    if st.session_state[f"{PAGE}.rank_by"] != "No ranking":
        st.radio(
            "**Sort order**",
            ["Ascending (Low to High)", "Descending (High to Low)"],
            index=1,
            key=f"{PAGE}.sort_order"
        )
