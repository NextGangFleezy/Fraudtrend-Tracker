import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import load_sample_data, filter_fraud_data
from utils.visualization import (
    create_fraud_type_chart, 
    create_heatmap, 
    create_geographic_map
)
from assets.images import get_image_url

# Page config
st.set_page_config(
    page_title="FraudLens - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_sample_data()

# Header with image
st.image(get_image_url("data visualization", 0), width=150)
st.title("Fraud Analytics Dashboard")
st.write("Interactive visualization of fraud trends and patterns")

# Create filters sidebar
st.sidebar.header("Dashboard Filters")

with st.sidebar.expander("Date Range", expanded=True):
    # Use default dates instead of None values
    from datetime import datetime, timedelta
    today = datetime.now().date()
    month_ago = today - timedelta(days=30)
    date_range = st.date_input(
        "Select Date Range",
        value=[month_ago, today],
        help="Filter data by date range"
    )

with st.sidebar.expander("Fraud Type", expanded=True):
    fraud_types = ["Identity Theft", "Payment Fraud", "Account Takeover", 
                   "Synthetic Identity", "Wire Fraud", "Loan Fraud"]
    selected_types = st.multiselect("Select Fraud Types", fraud_types)

with st.sidebar.expander("Risk Level", expanded=True):
    risk_levels = ["Low", "Medium", "High", "Critical"]
    selected_risks = st.multiselect("Select Risk Levels", risk_levels)

with st.sidebar.expander("Region", expanded=True):
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
    selected_regions = st.multiselect("Select Regions", regions)

# Apply filters button
apply_filters = st.sidebar.button("Apply Filters", use_container_width=True)

# Reset filters button
reset_filters = st.sidebar.button("Reset Filters", use_container_width=True)

# Main dashboard layout
# First row of visualizations
st.header("Fraud Overview")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud Cases by Type")
    fraud_type_chart = create_fraud_type_chart(st.session_state.data)
    st.plotly_chart(fraud_type_chart, use_container_width=True, key="fraud_type_chart")

with col2:
    st.subheader("Trend by Month")
    date_trend_chart = go.Figure()
    date_trend_chart.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    date_trend_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(date_trend_chart, use_container_width=True, key="date_trend_chart")

# Second row of visualizations
st.header("Detailed Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Level Distribution")
    risk_chart = go.Figure()
    risk_chart.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    risk_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(risk_chart, use_container_width=True, key="risk_level_chart")

with col2:
    st.subheader("Amount Distribution")
    amount_chart = go.Figure()
    amount_chart.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    amount_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(amount_chart, use_container_width=True, key="amount_distribution_chart")

# Geographic distribution
st.header("Geographic Distribution")
geo_map = create_geographic_map(st.session_state.data)
st.plotly_chart(geo_map, use_container_width=True, key="geographic_map")

# Heatmap analysis
st.header("Correlation Analysis")
heatmap_options = st.columns(3)
with heatmap_options[0]:
    x_var = st.selectbox("X-axis", ["Fraud Type", "Risk Level", "Detection Method", "Region"])
with heatmap_options[1]:
    y_var = st.selectbox("Y-axis", ["Risk Level", "Fraud Type", "Detection Method", "Region"])
with heatmap_options[2]:
    z_var = st.selectbox("Value", ["Count", "Average Amount", "Max Amount"])

heatmap = create_heatmap(st.session_state.data, x_var, y_var, z_var)
st.plotly_chart(heatmap, use_container_width=True, key="heatmap_analysis")

# Export options
st.header("Export Options")
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    export_format = st.selectbox("Export format", ["CSV", "Excel", "JSON"])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Export Dashboard Data", help="Download the current dashboard data in the selected format")

# Footer
st.markdown("---")
st.caption("FraudLens Dashboard: Interactive visualization of fraud trends and patterns")
