import streamlit as st
from utils.data_processing import load_sample_data, search_fraud_data
from utils.visualization import create_overview_chart
from assets.images import get_image_url

# Configure page settings
st.set_page_config(
    page_title="FraudLens - Fraud Trend Analysis",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_sample_data()
    
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
    
if 'filter_options' not in st.session_state:
    st.session_state.filter_options = {
        "fraud_type": [],
        "date_range": [None, None],
        "amount_range": [0, 1000000],
        "risk_level": []
    }

# Application header with image
st.image(get_image_url("cybersecurity", 0), width=120)
st.title("FraudLens")
st.subheader("A centralized fraud trend analysis platform")

# Main search bar
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        search_query = st.text_input(
            "Search fraud cases, patterns, or keywords",
            value=st.session_state.search_query,
            help="Enter keywords, case IDs, or fraud patterns to search"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search", use_container_width=True)
        
    if search_button and search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.rerun()

# Main dashboard overview
st.header("Fraud Trend Overview")

# Display key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Cases", f"{len(st.session_state.data):,}", delta="5%")
with col2:
    st.metric("Avg. Loss Amount", "$12,450", delta="-2%")
with col3:
    st.metric("Current Month Cases", "245", delta="7%")
with col4:
    st.metric("Detection Rate", "67%", delta="3%")

# Display overview chart
st.subheader("Fraud Trends Over Time")
overview_chart = create_overview_chart(st.session_state.data)
st.plotly_chart(overview_chart, use_container_width=True)

# Quick links to main sections
st.header("Navigate to Analysis Tools")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(get_image_url("fraud investigation", 0), width=150)
    st.markdown("### Case Explorer")
    st.write("Search and analyze individual fraud cases in detail")
    st.page_link("pages/case_explorer.py", label="Open Case Explorer", icon="🔍")

with col2:
    st.image(get_image_url("data visualization", 0), width=150)
    st.markdown("### Dashboard")
    st.write("View interactive visualization of fraud trends")
    st.page_link("pages/dashboard.py", label="View Dashboard", icon="📊")

with col3:
    st.image(get_image_url("data visualization", 1), width=150)
    st.markdown("### Pattern Analysis")
    st.write("Identify common fraud patterns and similarities")
    st.page_link("pages/pattern_analysis.py", label="Analyze Patterns", icon="🧩")

with col4:
    st.image(get_image_url("cybersecurity", 1), width=150)
    st.markdown("### Trend Analysis")
    st.write("Track and forecast emerging fraud trends")
    st.page_link("pages/trend_analysis.py", label="View Trends", icon="📈")

# Recent search results if a search was performed
if st.session_state.search_query:
    st.header(f"Search Results for '{st.session_state.search_query}'")
    search_results = search_fraud_data(st.session_state.data, st.session_state.search_query)
    
    if not search_results.empty:
        st.dataframe(search_results, use_container_width=True)
        
        # Export options
        col1, col2 = st.columns([1, 5])
        with col1:
            export_format = st.selectbox("Export format", ["CSV", "Excel", "JSON"])
        with col2:
            st.button("Export Results", help="Download the search results in the selected format")
    else:
        st.info("No results found. Try different search terms or browse the case explorer.")
        
# Footer
st.markdown("---")
st.caption("FraudLens: Improving investigation efficiency through data visualization and pattern recognition")
