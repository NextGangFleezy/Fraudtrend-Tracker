import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import load_sample_data, search_fraud_data, get_case_details
from utils.pattern_recognition import find_similar_cases
from assets.images import get_image_url

# Page config
st.set_page_config(
    page_title="FraudLens - Case Explorer",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_sample_data()

if 'selected_case' not in st.session_state:
    st.session_state.selected_case = None

# Header with image
st.image(get_image_url("fraud investigation", 1), width=150)
st.title("Case Explorer")
st.write("Search and analyze individual fraud cases in detail")

# Create search and filter sidebar
st.sidebar.header("Search & Filters")

search_query = st.sidebar.text_input(
    "Search cases",
    help="Search by case ID, keywords, or fraud type"
)

with st.sidebar.expander("Date Range", expanded=True):
    # Use default dates instead of None values
    from datetime import datetime, timedelta
    today = datetime.now().date()
    month_ago = today - timedelta(days=30)
    date_range = st.date_input(
        "Select Date Range",
        value=[month_ago, today],
        help="Filter cases by date range"
    )

with st.sidebar.expander("Fraud Type", expanded=True):
    fraud_types = ["Identity Theft", "Payment Fraud", "Account Takeover", 
                   "Synthetic Identity", "Wire Fraud", "Loan Fraud"]
    selected_types = st.multiselect("Select Fraud Types", fraud_types)

with st.sidebar.expander("Risk Level", expanded=True):
    risk_levels = ["Low", "Medium", "High", "Critical"]
    selected_risks = st.multiselect("Select Risk Levels", risk_levels)

with st.sidebar.expander("Status", expanded=True):
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    selected_statuses = st.multiselect("Select Status", statuses)

# Apply search button
search_button = st.sidebar.button("Search Cases", use_container_width=True)

# Reset filters button
reset_button = st.sidebar.button("Reset Filters", use_container_width=True)

# Main content area
if st.session_state.selected_case is None:
    # Display cases table
    st.header("Fraud Cases")
    
    # This would show actual search results in a real application
    st.info("Case data will appear when loaded or searched")
    
    # Sample empty table structure
    empty_table = pd.DataFrame(
        [], columns=['Case ID', 'Date', 'Type', 'Amount', 'Risk Level', 'Status']
    )
    st.dataframe(empty_table, use_container_width=True)
    
    # Case selection (would be populated with real options in production)
    case_selection = st.text_input("Enter Case ID to view details")
    view_case = st.button("View Case Details")
    
    if view_case and case_selection:
        st.session_state.selected_case = case_selection
        st.rerun()
else:
    # Display case details
    st.header(f"Case Details: {st.session_state.selected_case}")
    
    # Back button
    if st.button("← Back to Cases List"):
        st.session_state.selected_case = None
        st.rerun()
    
    # Create tabs for different aspects of the case
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Timeline", "Similar Cases", "Documentation"])
    
    with tab1:
        # Overview tab
        st.subheader("Case Overview")
        
        # Case details cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### Case Information")
            st.markdown("**Case ID:** (Case ID would appear here)")
            st.markdown("**Detected:** (Date would appear here)")
            st.markdown("**Status:** (Status would appear here)")
            st.markdown("**Risk Level:** (Risk level would appear here)")
        
        with col2:
            st.markdown("##### Fraud Details")
            st.markdown("**Type:** (Fraud type would appear here)")
            st.markdown("**Amount:** (Amount would appear here)")
            st.markdown("**Region:** (Region would appear here)")
            st.markdown("**Detection Method:** (Method would appear here)")
            
        with col3:
            st.markdown("##### Key Metrics")
            st.markdown("**Similar Cases:** (Count would appear here)")
            st.markdown("**Pattern Match:** (Score would appear here)")
            st.markdown("**Risk Score:** (Score would appear here)")
            st.markdown("**Days Open:** (Days would appear here)")
        
        # Case summary
        st.subheader("Case Summary")
        st.info("Case summary would appear here in a real application")
        
        # Case visualization
        st.subheader("Case Visualization")
        
        case_viz = go.Figure()
        case_viz.update_layout(
            title="Case Timeline and Events",
            template="plotly_dark",
            height=300,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        case_viz.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text="Visualization will appear when case is loaded",
            showarrow=False,
            font=dict(size=14)
        )
        st.plotly_chart(case_viz, use_container_width=True)
    
    with tab2:
        # Timeline tab
        st.subheader("Case Timeline")
        st.info("Timeline would display chronological events related to this case")
        
        # Timeline placeholder visualization
        timeline = go.Figure()
        timeline.update_layout(
            title="Case Timeline",
            template="plotly_dark",
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        timeline.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text="Timeline will appear when case is loaded",
            showarrow=False,
            font=dict(size=14)
        )
        st.plotly_chart(timeline, use_container_width=True)
    
    with tab3:
        # Similar Cases tab
        st.subheader("Similar Cases")
        st.info("This section would show cases with similar patterns or characteristics")
        
        # Similarity filters
        col1, col2, col3 = st.columns(3)
        with col1:
            similarity_threshold = st.slider("Minimum Similarity Score", 0.0, 1.0, 0.7)
        with col2:
            max_results = st.number_input("Max Results", 5, 50, 10)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            find_similar = st.button("Find Similar Cases")
        
        # Similar cases table (would be populated with real data in production)
        empty_similar = pd.DataFrame(
            [], columns=['Case ID', 'Similarity Score', 'Fraud Type', 'Amount', 'Date']
        )
        st.dataframe(empty_similar, use_container_width=True)
        
        # Similarity network visualization
        st.subheader("Case Similarity Network")
        network_viz = go.Figure()
        network_viz.update_layout(
            template="plotly_dark",
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        network_viz.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text="Similarity network will appear when case is loaded",
            showarrow=False,
            font=dict(size=14)
        )
        st.plotly_chart(network_viz, use_container_width=True)
    
    with tab4:
        # Documentation tab
        st.subheader("Case Documentation")
        st.info("This section would contain notes, documents, and evidence related to the case")
        
        # Notes section
        st.markdown("##### Case Notes")
        notes_area = st.text_area("Add notes to this case", height=150)
        st.button("Save Notes")
        
        # Attachments section
        st.markdown("##### Attachments")
        st.info("Attachments would be listed here in a real application")
        
        # Actions section
        st.markdown("##### Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Update Status")
        with col2:
            st.button("Add Documentation")
        with col3:
            st.button("Export Case Report")

# Footer
st.markdown("---")
st.caption("FraudLens Case Explorer: Detailed analysis of individual fraud cases")
