import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import load_sample_data, prepare_time_series_data
from utils.visualization import create_trend_forecast
from assets.images import get_image_url

# Page config
st.set_page_config(
    page_title="FraudLens - Trend Analysis",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_sample_data()

# Header with image
st.image(get_image_url("data visualization", 2), width=150)
st.title("Fraud Trend Analysis")
st.write("Track, analyze, and forecast emerging fraud trends")

# Sidebar controls
st.sidebar.header("Trend Analysis Settings")

# Time settings
time_unit = st.sidebar.selectbox(
    "Time Grouping",
    ["Day", "Week", "Month", "Quarter", "Year"],
    index=2  # Default to Month
)

# Date range 
with st.sidebar.expander("Date Range", expanded=True):
    trend_date_range = st.date_input(
        "Select Date Range",
        value=[None, None],
        help="Analyze trends within this date range"
    )

# Trend variables
with st.sidebar.expander("Trend Variables", expanded=True):
    trend_metric = st.selectbox(
        "Primary Metric",
        ["Number of Cases", "Total Amount", "Average Amount", "Detection Rate"]
    )
    
    breakdown_variable = st.selectbox(
        "Breakdown By",
        ["None", "Fraud Type", "Risk Level", "Region", "Detection Method"]
    )

# Forecast settings
with st.sidebar.expander("Forecast Settings", expanded=True):
    show_forecast = st.checkbox("Show Forecast", value=True)
    
    if show_forecast:
        forecast_periods = st.number_input("Forecast Periods", 1, 24, 6)
        confidence_interval = st.slider("Confidence Interval (%)", 50, 95, 80)

# Apply settings button
apply_button = st.sidebar.button("Update Trends", use_container_width=True)

# Main content area
st.header("Fraud Trend Overview")

# Overall trend chart
overall_trend = create_trend_forecast(st.session_state.data, forecast_periods=6 if show_forecast else 0)
st.plotly_chart(overall_trend, use_container_width=True)

# Trend metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Period", "(Value would appear here)", delta="(Change would appear here)")
with col2:
    st.metric("Trend Direction", "(Direction would appear here)", delta="(Change would appear here)")
with col3:
    st.metric("Forecast Next Period", "(Value would appear here)", delta="(Change would appear here)")
with col4:
    st.metric("Seasonality Detected", "(Yes/No would appear here)")

# Breakdown analysis
if breakdown_variable != "None":
    st.header(f"Trend Breakdown by {breakdown_variable}")
    
    breakdown_chart = go.Figure()
    breakdown_chart.update_layout(
        title=f"{trend_metric} by {breakdown_variable} Over Time",
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    breakdown_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Breakdown visualization would appear here",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(breakdown_chart, use_container_width=True)
    
    # Breakdown metrics
    st.subheader("Key Insights")
    
    metrics_cols = st.columns(3)
    with metrics_cols[0]:
        st.info("Fastest growing category would appear here")
    with metrics_cols[1]:
        st.info("Most declining category would appear here")
    with metrics_cols[2]:
        st.info("Most volatile category would appear here")

# Seasonal analysis
st.header("Seasonal Patterns")

seasonal_chart = go.Figure()
seasonal_chart.update_layout(
    title="Seasonal Fraud Patterns",
    template="plotly_dark",
    height=400,
    margin=dict(l=40, r=40, t=40, b=40)
)
seasonal_chart.add_annotation(
    x=0.5, y=0.5,
    xref="paper", yref="paper",
    text="Seasonal pattern visualization would appear here",
    showarrow=False,
    font=dict(size=14)
)
st.plotly_chart(seasonal_chart, use_container_width=True)

# Seasonal insights
col1, col2 = st.columns(2)
with col1:
    st.subheader("Seasonal Peaks")
    st.info("Information about seasonal peaks would appear here")
with col2:
    st.subheader("Seasonal Lows")
    st.info("Information about seasonal lows would appear here")

# Advanced trend analysis
st.header("Advanced Trend Analysis")

# Tabs for different analyses
tab1, tab2, tab3 = st.tabs(["Correlation Analysis", "Growth Rates", "Trend Decomposition"])

with tab1:
    st.subheader("Correlation with External Factors")
    
    # Correlation settings
    col1, col2, col3 = st.columns(3)
    with col1:
        corr_factor = st.selectbox(
            "External Factor",
            ["Economic Indicators", "Holiday Periods", "Regulatory Changes", "Data Breaches"]
        )
    with col2:
        lag_periods = st.number_input("Lag Periods", 0, 12, 1)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_corr = st.button("Analyze Correlation")
    
    # Correlation chart
    corr_chart = go.Figure()
    corr_chart.update_layout(
        title="Correlation Analysis",
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    corr_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Correlation visualization would appear here",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(corr_chart, use_container_width=True)

with tab2:
    st.subheader("Growth Rate Analysis")
    
    # Growth rate chart
    growth_chart = go.Figure()
    growth_chart.update_layout(
        title="Growth Rate Over Time",
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    growth_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Growth rate visualization would appear here",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(growth_chart, use_container_width=True)
    
    # Growth insights
    st.info("Growth rate insights would appear here")

with tab3:
    st.subheader("Trend Decomposition")
    
    # Decomposition chart
    decomp_chart = go.Figure()
    decomp_chart.update_layout(
        title="Trend Decomposition",
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    decomp_chart.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Trend decomposition visualization would appear here",
        showarrow=False,
        font=dict(size=14)
    )
    st.plotly_chart(decomp_chart, use_container_width=True)
    
    # Decomposition insights
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Trend Component")
        st.info("Trend component insights would appear here")
    with col2:
        st.markdown("##### Seasonal Component")
        st.info("Seasonal component insights would appear here")

# Export options
st.header("Export Options")
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    export_format = st.selectbox("Export format", ["CSV", "Excel", "JSON"])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Export Trend Analysis", help="Download the current trend analysis in the selected format")

# Footer
st.markdown("---")
st.caption("FraudLens Trend Analysis: Track and forecast emerging fraud trends")
