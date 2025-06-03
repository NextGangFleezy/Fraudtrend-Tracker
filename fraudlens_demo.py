import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import os

# Set page configuration
st.set_page_config(
    page_title="FraudLens Demo",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4F8BF9;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FAFAFA;
        margin-top: 0;
    }
    .metric-card {
        background-color: #1E2130;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .fraud-type-tag {
        background-color: #4F8BF9;
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    .risk-high {
        color: #FF4B4B;
        font-weight: bold;
    }
    .risk-medium {
        color: #FFA500;
        font-weight: bold;
    }
    .risk-low {
        color: #00CC96;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare demo data
@st.cache_data
def load_demo_data():
    # Check if we have the custom data file
    if os.path.exists("attached_assets/fraud_test_data.json"):
        try:
            with open("attached_assets/fraud_test_data.json", "r") as f:
                custom_data = json.load(f)
            
            # Convert to DataFrame
            custom_df = pd.DataFrame(custom_data)
            
            # Add necessary fields
            custom_df['detection_date'] = pd.to_datetime(custom_df['date'])
            custom_df['reported_amount'] = [random.randint(500, 5000) for _ in range(len(custom_df))]
            custom_df['fraud_type'] = custom_df['tags'].apply(lambda x: x[0].title() if x else "Unknown")
            custom_df['risk_level'] = custom_df['status'].map({
                'confirmed_fraud': 'High',
                'false_positive': 'Low',
                'under_investigation': 'Medium'
            }).fillna('Medium')
            custom_df['region'] = ['North America', 'Europe', 'Asia', 'South America', 'Australia'][
                np.random.randint(0, 5, size=len(custom_df))
            ]
            
            base_data = custom_df
        except:
            # If loading fails, create demo data
            base_data = pd.DataFrame()
    else:
        base_data = pd.DataFrame()
    
    # If we couldn't load the file or it had issues, generate completely synthetic data
    if base_data.empty:
        # Create synthetic fraud types
        fraud_types = ['Phishing', 'Card Skimming', 'Identity Theft', 'Account Takeover', 
                       'Synthetic Identity', 'Merchant Fraud', 'Wire Fraud', 'Check Fraud']
        
        # Create regions
        regions = ['North America', 'Europe', 'Asia', 'South America', 'Australia']
        
        # Create risk levels
        risk_levels = ['High', 'Medium', 'Low']
        
        # Create detection methods
        detection_methods = ['Machine Learning', 'Customer Report', 'Manual Review', 
                             'Rule-Based System', 'Threshold Alert']
        
        # Generate dates spanning last 12 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        
        # Generate random data
        n_samples = 200
        data = {
            'case_id': [f'FR-{i:06d}' for i in range(1, n_samples + 1)],
            'detection_date': np.random.choice(dates, n_samples),
            'fraud_type': np.random.choice(fraud_types, n_samples, p=[0.3, 0.2, 0.15, 0.1, 0.05, 0.1, 0.05, 0.05]),
            'reported_amount': np.random.lognormal(7, 1, n_samples).astype(int),
            'risk_level': np.random.choice(risk_levels, n_samples, p=[0.3, 0.5, 0.2]),
            'status': np.random.choice(['Confirmed', 'In Progress', 'Closed'], n_samples, p=[0.4, 0.4, 0.2]),
            'region': np.random.choice(regions, n_samples),
            'detection_method': np.random.choice(detection_methods, n_samples),
            'case_summary': [f'Suspicious activity detected involving {np.random.choice(fraud_types)} ' +
                             f'in {np.random.choice(regions)}. ' +
                             f'Amount: ${np.random.randint(100, 10000)}.' for _ in range(n_samples)]
        }
        
        base_data = pd.DataFrame(data)
    
    # Generate more data for a fuller demonstration - always add this
    n_additional = 150
    fraud_types = ['Phishing', 'Card Skimming', 'Identity Theft', 'Account Takeover', 
                   'Synthetic Identity', 'Merchant Fraud', 'Wire Fraud', 'Check Fraud']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Australia']
    risk_levels = ['High', 'Medium', 'Low']
    detection_methods = ['Machine Learning', 'Customer Report', 'Manual Review', 
                         'Rule-Based System', 'Threshold Alert']
    
    # Generate dates spanning last 12 months with distribution that shows an increase in recent months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Create a distribution that favors more recent dates (more fraud cases recently)
    date_weights = np.linspace(0.5, 10, 12)
    months = pd.date_range(start=start_date, end=end_date, freq='MS')
    month_indices = np.random.choice(range(len(months)), n_additional, p=date_weights/sum(date_weights))
    dates = [months[i] + timedelta(days=np.random.randint(0, 28)) for i in month_indices]
    
    additional_data = {
        'case_id': [f'GEN-{i:06d}' for i in range(1, n_additional + 1)],
        'detection_date': dates,
        'fraud_type': np.random.choice(fraud_types, n_additional, p=[0.3, 0.2, 0.15, 0.1, 0.05, 0.1, 0.05, 0.05]),
        'reported_amount': np.random.lognormal(7, 1, n_additional).astype(int),
        'risk_level': np.random.choice(risk_levels, n_additional, p=[0.3, 0.5, 0.2]),
        'status': np.random.choice(['Confirmed', 'In Progress', 'Closed'], n_additional, p=[0.4, 0.4, 0.2]),
        'region': np.random.choice(regions, n_additional),
        'detection_method': np.random.choice(detection_methods, n_additional),
        'case_summary': [f'Suspicious activity detected involving {np.random.choice(fraud_types)} ' +
                         f'in {np.random.choice(regions)}. ' +
                         f'Amount: ${np.random.randint(100, 10000)}.' for _ in range(n_additional)]
    }
    
    additional_df = pd.DataFrame(additional_data)
    
    # Combine base data with additional data
    combined_df = pd.concat([base_data, additional_df], ignore_index=True)
    
    # Ensure detection_date is datetime
    combined_df['detection_date'] = pd.to_datetime(combined_df['detection_date'])
    
    # Sort by detection_date
    combined_df = combined_df.sort_values('detection_date', ascending=False)
    
    return combined_df

# Load demo data
fraud_data = load_demo_data()

# Create time-series chart
def create_trend_chart(df):
    # Group by month and count cases
    df['month'] = df['detection_date'].dt.strftime('%Y-%m')
    monthly_counts = df.groupby('month').size().reset_index(name='count')
    
    # Create line chart
    fig = px.line(
        monthly_counts, 
        x='month', 
        y='count',
        markers=True,
        title="Fraud Cases Over Time",
        labels={"month": "Month", "count": "Number of Cases"}
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified"
    )
    
    return fig

# Create fraud type breakdown chart
def create_type_chart(df):
    type_counts = df['fraud_type'].value_counts().reset_index()
    type_counts.columns = ['fraud_type', 'count']
    
    fig = px.bar(
        type_counts.sort_values('count', ascending=False),
        x='fraud_type',
        y='count',
        title="Fraud Cases by Type",
        labels={"fraud_type": "Fraud Type", "count": "Number of Cases"},
        color='count',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    return fig

# Create risk level pie chart
def create_risk_chart(df):
    risk_counts = df['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['risk_level', 'count']
    
    fig = px.pie(
        risk_counts,
        values='count',
        names='risk_level',
        title="Risk Level Distribution",
        color='risk_level',
        color_discrete_map={'High': '#FF4B4B', 'Medium': '#FFA500', 'Low': '#00CC96'}
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    return fig

# Create region map
def create_region_chart(df):
    region_counts = df['region'].value_counts().reset_index()
    region_counts.columns = ['region', 'count']
    
    # Map regions to coordinates (approximate centers)
    region_coords = {
        'North America': {'lat': 40, 'lon': -100},
        'South America': {'lat': -15, 'lon': -60},
        'Europe': {'lat': 50, 'lon': 10},
        'Asia': {'lat': 35, 'lon': 100},
        'Australia': {'lat': -25, 'lon': 135},
        'Africa': {'lat': 0, 'lon': 20}
    }
    
    # Create dataframe with coordinates
    map_data = pd.DataFrame([
        {
            'region': region,
            'count': count,
            'lat': region_coords.get(region, {'lat': 0, 'lon': 0})['lat'],
            'lon': region_coords.get(region, {'lat': 0, 'lon': 0})['lon'],
            'size': count / max(region_counts['count']) * 30 + 10  # Size proportional to count
        }
        for region, count in zip(region_counts['region'], region_counts['count'])
    ])
    
    fig = px.scatter_geo(
        map_data,
        lat='lat',
        lon='lon',
        size='size',
        color='count',
        hover_name='region',
        text='region',
        title="Fraud Cases by Region",
        projection='natural earth',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    fig.update_traces(
        textposition='top center',
        marker=dict(line=dict(width=1, color='DarkSlateGrey'))
    )
    
    return fig

# Function to find similar cases
def find_similar_cases(case_id, df, top_n=5):
    # Get the target case
    target_case = df[df['case_id'] == case_id].iloc[0]
    
    # Simple similarity calculation based on fraud type and region
    df_copy = df[df['case_id'] != case_id].copy()
    
    # Calculate similarity scores (very simplified)
    df_copy['similarity'] = 0
    
    # Same fraud type is a strong signal
    df_copy.loc[df_copy['fraud_type'] == target_case['fraud_type'], 'similarity'] += 50
    
    # Same region is a moderate signal
    df_copy.loc[df_copy['region'] == target_case['region'], 'similarity'] += 30
    
    # Same risk level is a weak signal
    df_copy.loc[df_copy['risk_level'] == target_case['risk_level'], 'similarity'] += 20
    
    # Temporal proximity (cases within 30 days)
    days_diff = abs((df_copy['detection_date'] - target_case['detection_date']).dt.days)
    df_copy['similarity'] += np.maximum(0, 30 - days_diff/2)  # Up to 30 points for very close dates
    
    # Return top N similar cases
    return df_copy.sort_values('similarity', ascending=False).head(top_n)

# Define sidebar for navigation
st.sidebar.markdown("<h1 style='text-align: center;'>FraudLens</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>Fraud Analysis Platform</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Case Explorer", "Pattern Analysis", "Trend Forecasting"])

# Add sidebar filters that apply to all pages
st.sidebar.markdown("## Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(fraud_data['detection_date'].min().date(), fraud_data['detection_date'].max().date()),
    min_value=fraud_data['detection_date'].min().date(),
    max_value=fraud_data['detection_date'].max().date()
)

# Fraud type filter
fraud_types = ['All Types'] + sorted(fraud_data['fraud_type'].unique().tolist())
selected_type = st.sidebar.selectbox("Fraud Type", fraud_types)

# Risk level filter
risk_levels = ['All Levels'] + sorted(fraud_data['risk_level'].unique().tolist())
selected_risk = st.sidebar.selectbox("Risk Level", risk_levels)

# Apply filters
filtered_data = fraud_data.copy()

# Date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_data = filtered_data[
        (filtered_data['detection_date'].dt.date >= start_date) & 
        (filtered_data['detection_date'].dt.date <= end_date)
    ]

# Type filter
if selected_type != 'All Types':
    filtered_data = filtered_data[filtered_data['fraud_type'] == selected_type]

# Risk filter
if selected_risk != 'All Levels':
    filtered_data = filtered_data[filtered_data['risk_level'] == selected_risk]

# Add "Demo" tag to header with theme-aware styling
st.markdown(f"<div style='background-color: var(--primary-color); padding: 5px; border-radius: 5px; width: fit-content;'><span style='color: white; font-weight: bold;'>DEMO</span></div>", unsafe_allow_html=True)

# Dashboard page
if page == "Dashboard":
    st.markdown("<h1 class='main-header'>Fraud Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Real-time insights into fraud trends and patterns</p>", unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Cases", f"{len(filtered_data):,}", 
                  delta=f"{int(len(filtered_data)*0.05):+,}" if len(filtered_data) > 0 else "0")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        avg_amount = int(filtered_data['reported_amount'].mean()) if not filtered_data.empty else 0
        st.metric("Avg. Loss Amount", f"${avg_amount:,}", 
                  delta=f"{int(avg_amount*0.02):+,}" if avg_amount > 0 else "0")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        high_risk = len(filtered_data[filtered_data['risk_level'] == 'High']) if not filtered_data.empty else 0
        st.metric("High Risk Cases", f"{high_risk:,}", 
                  delta=f"{int(high_risk*0.1):+,}" if high_risk > 0 else "0")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        detection_rate = int(len(filtered_data[filtered_data['status'] == 'Confirmed'])/max(1, len(filtered_data))*100)
        st.metric("Detection Rate", f"{detection_rate}%", 
                  delta=f"{int(detection_rate*0.05):+}%" if detection_rate > 0 else "0%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("### Fraud Trends and Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        trend_chart = create_trend_chart(filtered_data)
        st.plotly_chart(trend_chart, use_container_width=True)
        
    with col2:
        type_chart = create_type_chart(filtered_data)
        st.plotly_chart(type_chart, use_container_width=True)
        
    col1, col2 = st.columns(2)
    
    with col1:
        risk_chart = create_risk_chart(filtered_data)
        st.plotly_chart(risk_chart, use_container_width=True)
        
    with col2:
        region_chart = create_region_chart(filtered_data)
        st.plotly_chart(region_chart, use_container_width=True)
    
    # Recent cases
    st.markdown("### Recent Fraud Cases")
    recent_cases = filtered_data.head(5)
    
    # Display cases in a more visual way
    for i, case in recent_cases.iterrows():
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown(f"**Case ID:** {case['case_id']}")
            st.markdown(f"**Date:** {case['detection_date'].strftime('%Y-%m-%d')}")
            
        with col2:
            st.markdown(f"**{case['case_summary']}**")
            st.markdown(f"<span class='fraud-type-tag'>{case['fraud_type']}</span> • Region: {case['region']}", 
                        unsafe_allow_html=True)
            
        with col3:
            risk_class = f"risk-{case['risk_level'].lower()}"
            st.markdown(f"**Risk:** <span class='{risk_class}'>{case['risk_level']}</span>", 
                        unsafe_allow_html=True)
            st.markdown(f"**Amount:** ${case['reported_amount']:,}")
            
        st.markdown("---")

# Case Explorer page
elif page == "Case Explorer":
    st.markdown("<h1 class='main-header'>Case Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Search and analyze individual fraud cases</p>", unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("Search for cases by ID, type, or description")
    
    if search_query:
        # Simple search implementation
        search_results = filtered_data[
            filtered_data['case_id'].str.contains(search_query, case=False, na=False) |
            filtered_data['fraud_type'].str.contains(search_query, case=False, na=False) |
            filtered_data['case_summary'].str.contains(search_query, case=False, na=False) |
            filtered_data['region'].str.contains(search_query, case=False, na=False)
        ]
        
        st.write(f"Found {len(search_results)} matching cases")
        
        # Display search results
        if not search_results.empty:
            st.dataframe(
                search_results[['case_id', 'detection_date', 'fraud_type', 'reported_amount', 
                               'risk_level', 'region', 'status']],
                use_container_width=True
            )
    
    # Case details
    st.markdown("### Case Details")
    
    selected_case_id = st.selectbox(
        "Select a case to view details", 
        filtered_data['case_id'].tolist()
    )
    
    if selected_case_id:
        case = filtered_data[filtered_data['case_id'] == selected_case_id].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Case Information")
            st.markdown(f"**Case ID:** {case['case_id']}")
            st.markdown(f"**Detection Date:** {case['detection_date'].strftime('%Y-%m-%d')}")
            st.markdown(f"**Fraud Type:** {case['fraud_type']}")
            st.markdown(f"**Region:** {case['region']}")
            
            risk_class = f"risk-{case['risk_level'].lower()}"
            st.markdown(f"**Risk Level:** <span class='{risk_class}'>{case['risk_level']}</span>", 
                        unsafe_allow_html=True)
            
            st.markdown(f"**Status:** {case['status']}")
            st.markdown(f"**Reported Amount:** ${case['reported_amount']:,}")
            st.markdown(f"**Detection Method:** {case['detection_method']}")
            
        with col2:
            st.markdown("#### Case Summary")
            st.write(case['case_summary'])
            
            st.markdown("#### Similar Cases")
            similar_cases = find_similar_cases(selected_case_id, filtered_data)
            
            # Display similarity score with a gauge chart for each similar case
            for i, sim_case in similar_cases.iterrows():
                col1, col2, col3 = st.columns([2, 7, 1])
                
                with col1:
                    # Create a gauge chart for similarity score
                    similarity = int(sim_case['similarity'])
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=similarity,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': f"rgba({255 - 2.55*similarity}, {2.55*similarity}, 0, 0.8)"},
                            'steps': [
                                {'range': [0, 40], 'color': "lightgray"},
                                {'range': [40, 70], 'color': "gray"},
                                {'range': [70, 100], 'color': "darkgray"}
                            ]
                        },
                        number={'suffix': "%"}
                    ))
                    
                    fig.update_layout(
                        height=100,
                        margin=dict(l=10, r=10, t=10, b=10),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown(f"**{sim_case['case_id']}** - {sim_case['detection_date'].strftime('%Y-%m-%d')}")
                    st.markdown(f"<span class='fraud-type-tag'>{sim_case['fraud_type']}</span> • Region: {sim_case['region']}", 
                                unsafe_allow_html=True)
                    st.markdown(f"{sim_case['case_summary'][:100]}...")
                    
                with col3:
                    risk_class = f"risk-{sim_case['risk_level'].lower()}"
                    st.markdown(f"<span class='{risk_class}'>{sim_case['risk_level']}</span>", 
                                unsafe_allow_html=True)
                    
                st.markdown("---")
            
            # Action buttons (for demo purposes only)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Export Case Details")
            with col2:
                st.button("Mark for Review")
            with col3:
                st.button("Update Case Status")

# Pattern Analysis page
elif page == "Pattern Analysis":
    st.markdown("<h1 class='main-header'>Pattern Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Identify fraud patterns and clusters</p>", unsafe_allow_html=True)
    
    # Pattern visualization with demo clustering
    st.markdown("### Fraud Pattern Clusters")
    
    # Demo cluster visualization
    def create_cluster_visualization(df):
        # This is a simulated clustering for demo purposes
        # In a real implementation, this would use actual machine learning algorithms
        
        # Assign cluster IDs based on fraud type and risk level
        df_copy = df.copy()
        
        # Create a mapping of fraud types to cluster centers
        fraud_types = df_copy['fraud_type'].unique()
        cluster_centers = {}
        
        for i, fraud_type in enumerate(fraud_types):
            angle = 2 * np.pi * i / len(fraud_types)
            cluster_centers[fraud_type] = {
                'x': np.cos(angle) * 5,
                'y': np.sin(angle) * 5
            }
        
        # Assign coordinates with some noise
        df_copy['cluster_x'] = df_copy['fraud_type'].map(lambda x: cluster_centers[x]['x']) + np.random.normal(0, 1, len(df_copy))
        df_copy['cluster_y'] = df_copy['fraud_type'].map(lambda x: cluster_centers[x]['y']) + np.random.normal(0, 1, len(df_copy))
        
        # Adjust coordinates based on risk level
        risk_offset = {'High': 0.5, 'Medium': 0, 'Low': -0.5}
        df_copy['cluster_x'] += df_copy['risk_level'].map(risk_offset)
        df_copy['cluster_y'] += df_copy['risk_level'].map(risk_offset)
        
        # Color by fraud type
        fig = px.scatter(
            df_copy, 
            x='cluster_x', 
            y='cluster_y', 
            color='fraud_type',
            size='reported_amount',
            size_max=15,
            hover_name='case_id',
            hover_data=['detection_date', 'risk_level', 'reported_amount'],
            title="Fraud Pattern Clusters",
            labels={'cluster_x': '', 'cluster_y': ''}
        )
        
        # Update to clean layout
        fig.update_layout(
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        
        # Add fraud type labels at cluster centers
        for fraud_type, center in cluster_centers.items():
            fig.add_annotation(
                x=center['x'],
                y=center['y'],
                text=fraud_type,
                showarrow=False,
                font=dict(size=14, color='black'),
                bgcolor='rgba(255, 255, 255, 0.7)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                borderpad=4
            )
        
        return fig
    
    cluster_fig = create_cluster_visualization(filtered_data)
    st.plotly_chart(cluster_fig, use_container_width=True)
    
    # Pattern insights
    st.markdown("### Pattern Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Fraud Type Correlations")
        
        # Create a demo correlation matrix
        fraud_types = filtered_data['fraud_type'].unique()
        corr_matrix = np.random.rand(len(fraud_types), len(fraud_types))
        np.fill_diagonal(corr_matrix, 1)
        
        # Make it symmetric for a realistic correlation matrix
        corr_matrix = (corr_matrix + corr_matrix.T) / 2
        
        # Create heatmap
        corr_df = pd.DataFrame(corr_matrix, index=fraud_types, columns=fraud_types)
        
        fig = px.imshow(
            corr_df,
            title="Fraud Type Correlations",
            color_continuous_scale='Blues',
            zmin=0, zmax=1
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### Anomaly Detection")
        
        # Demo anomaly score calculation
        df_copy = filtered_data.copy()
        
        # Use reported amount as a proxy for anomaly score
        df_copy['anomaly_score'] = np.random.uniform(0, 1, len(df_copy))
        
        # Higher amounts have higher anomaly scores
        df_copy['anomaly_score'] = df_copy['anomaly_score'] + (df_copy['reported_amount'] / df_copy['reported_amount'].max() * 0.5)
        df_copy['anomaly_score'] = df_copy['anomaly_score'].clip(0, 1)
        
        # Create histogram of anomaly scores
        fig = px.histogram(
            df_copy,
            x='anomaly_score',
            nbins=20,
            title="Distribution of Anomaly Scores",
            labels={'anomaly_score': 'Anomaly Score', 'count': 'Number of Cases'},
            color_discrete_sequence=['#4F8BF9']
        )
        
        # Add a vertical line for anomaly threshold
        fig.add_vline(x=0.8, line_dash="dash", line_color="red")
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show top anomalies
        st.markdown("#### Top Anomalous Cases")
        anomalies = df_copy.sort_values('anomaly_score', ascending=False).head(5)
        
        for i, case in anomalies.iterrows():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                # Create small gauge for anomaly score
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=case['anomaly_score'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': f"rgba({255*case['anomaly_score']}, {255*(1-case['anomaly_score'])}, 0, 0.8)"},
                    },
                    number={'suffix': "%"}
                ))
                
                fig.update_layout(
                    height=100,
                    margin=dict(l=5, r=5, t=5, b=5),
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"**{case['case_id']}** - {case['detection_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"<span class='fraud-type-tag'>{case['fraud_type']}</span> • ${case['reported_amount']:,}", 
                            unsafe_allow_html=True)
            
            st.markdown("---")

# Trend Forecasting page
elif page == "Trend Forecasting":
    st.markdown("<h1 class='main-header'>Trend Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Predict emerging fraud trends</p>", unsafe_allow_html=True)
    
    # Time period selector
    forecast_period = st.radio("Forecast Period", ["3 Months", "6 Months", "1 Year"], horizontal=True)
    
    # Convert to number of months for forecasting
    if forecast_period == "3 Months":
        months_ahead = 3
    elif forecast_period == "6 Months":
        months_ahead = 6
    else:
        months_ahead = 12
    
    # Create demo forecast
    def create_forecast_chart(df, months_ahead=6):
        # Group by month and count cases
        df['month'] = df['detection_date'].dt.strftime('%Y-%m')
        monthly_counts = df.groupby('month').size().reset_index(name='count')
        monthly_counts['date'] = pd.to_datetime(monthly_counts['month'] + '-01')
        monthly_counts = monthly_counts.sort_values('date')
        
        # Generate forecast dates
        last_date = monthly_counts['date'].max()
        forecast_dates = [last_date + pd.DateOffset(months=i+1) for i in range(months_ahead)]
        
        # Generate forecast values (simple trend + seasonal pattern + noise)
        if len(monthly_counts) >= 3:
            # Calculate trend
            counts = monthly_counts['count'].values
            trend = (counts[-1] - counts[0]) / max(1, len(counts) - 1)
            
            # Add some seasonality and noise
            forecast_values = [
                max(5, counts[-1] + trend * (i+1) + 
                   10 * np.sin(2 * np.pi * i / 12) +  # Seasonality
                   np.random.normal(0, max(2, counts[-1] * 0.1)))  # Noise
                for i in range(months_ahead)
            ]
        else:
            # Not enough data, use flat forecast with noise
            forecast_values = [
                max(5, monthly_counts['count'].mean() + np.random.normal(0, 5))
                for _ in range(months_ahead)
            ]
        
        # Round to integers
        forecast_values = [max(0, round(val)) for val in forecast_values]
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'count': forecast_values,
            'month': [d.strftime('%Y-%m') for d in forecast_dates],
            'type': 'Forecast'
        })
        
        # Add type to original data
        monthly_counts['type'] = 'Historical'
        
        # Combine historical and forecast
        combined_df = pd.concat([monthly_counts, forecast_df], ignore_index=True)
        
        # Create line chart
        fig = px.line(
            combined_df, 
            x='date', 
            y='count',
            color='type',
            markers=True,
            title="Fraud Trend Forecast",
            labels={"date": "Month", "count": "Number of Cases", "type": "Data Type"},
            color_discrete_map={'Historical': '#4F8BF9', 'Forecast': '#FF4B4B'}
        )
        
        # Add confidence interval for forecast
        forecast_section = combined_df[combined_df['type'] == 'Forecast']
        
        # Add upper and lower bounds (±20% for demo)
        upper_bound = [val * 1.2 for val in forecast_section['count']]
        lower_bound = [max(0, val * 0.8) for val in forecast_section['count']]
        
        fig.add_trace(
            go.Scatter(
                x=forecast_section['date'].tolist() + forecast_section['date'].tolist()[::-1],
                y=upper_bound + lower_bound[::-1],
                fill='toself',
                fillcolor='rgba(255, 75, 75, 0.2)',
                line=dict(color='rgba(255, 75, 75, 0)'),
                hoverinfo='skip',
                showlegend=False
            )
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig, forecast_df
    
    forecast_fig, forecast_data = create_forecast_chart(filtered_data, months_ahead)
    st.plotly_chart(forecast_fig, use_container_width=True)
    
    # Forecast insights
    st.markdown("### Forecast Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Projected Growth by Fraud Type")
        
        # Create demo growth projections by fraud type
        fraud_types = filtered_data['fraud_type'].unique()
        
        growth_data = []
        for fraud_type in fraud_types:
            # Random growth rate between -30% and +80%
            growth_rate = np.random.uniform(-0.3, 0.8)
            growth_data.append({
                'fraud_type': fraud_type,
                'growth_rate': growth_rate
            })
            
        growth_df = pd.DataFrame(growth_data)
        
        # Sort by growth rate
        growth_df = growth_df.sort_values('growth_rate', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            growth_df,
            x='fraud_type',
            y='growth_rate',
            title="Projected Growth Rate by Fraud Type",
            labels={"fraud_type": "Fraud Type", "growth_rate": "Projected Growth Rate"},
            color='growth_rate',
            color_continuous_scale=['red', 'yellow', 'green'],
            range_color=[-0.3, 0.8]
        )
        
        # Format y-axis as percentage
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            yaxis=dict(tickformat=".0%")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### Risk Level Forecast")
        
        # Create demo risk level forecast
        months = [pd.to_datetime(forecast_data['month'].iloc[i] + '-01').strftime('%b %Y') 
                 for i in range(len(forecast_data))]
        
        # Create random risk level distributions that sum to the forecast count
        high_risk = []
        medium_risk = []
        low_risk = []
        
        for count in forecast_data['count']:
            # Random distribution that sums to count
            high = max(0, int(count * np.random.uniform(0.2, 0.4)))
            medium = max(0, int(count * np.random.uniform(0.3, 0.5)))
            low = max(0, int(count - high - medium))
            
            high_risk.append(high)
            medium_risk.append(medium)
            low_risk.append(low)
        
        # Create stacked bar chart
        risk_forecast = pd.DataFrame({
            'Month': months,
            'High': high_risk,
            'Medium': medium_risk,
            'Low': low_risk
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=risk_forecast['Month'],
            y=risk_forecast['High'],
            name='High Risk',
            marker_color='#FF4B4B'
        ))
        
        fig.add_trace(go.Bar(
            x=risk_forecast['Month'],
            y=risk_forecast['Medium'],
            name='Medium Risk',
            marker_color='#FFA500'
        ))
        
        fig.add_trace(go.Bar(
            x=risk_forecast['Month'],
            y=risk_forecast['Low'],
            name='Low Risk',
            marker_color='#00CC96'
        ))
        
        fig.update_layout(
            barmode='stack',
            title="Risk Level Distribution Forecast",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Emerging threats
    st.markdown("### Emerging Fraud Threats")
    
    # Create demo emerging threats
    emerging_threats = [
        {
            "threat": "Synthetic Identity Fraud",
            "risk_level": "High",
            "trend": "Increasing",
            "description": "Fraudsters are increasingly combining real and fake information to create synthetic identities that pass traditional verification checks."
        },
        {
            "threat": "Voice Deepfake Scams",
            "risk_level": "High",
            "trend": "Rapidly Increasing",
            "description": "AI-generated voice cloning is being used to impersonate executives and customers in phone-based social engineering attacks."
        },
        {
            "threat": "QR Code Phishing",
            "risk_level": "Medium",
            "trend": "Emerging",
            "description": "Fraudulent QR codes are being placed in public locations to redirect users to credential harvesting sites."
        },
        {
            "threat": "Supply Chain Account Takeover",
            "risk_level": "Medium",
            "trend": "Steady",
            "description": "Compromising smaller vendors in the supply chain to gain access to larger, more secure organizations."
        }
    ]
    
    for threat in emerging_threats:
        col1, col2 = st.columns([1, 4])
        
        with col1:
            risk_class = f"risk-{threat['risk_level'].lower()}"
            
            st.markdown(f"**Risk:**")
            st.markdown(f"<span class='{risk_class}'>{threat['risk_level']}</span>", 
                        unsafe_allow_html=True)
            
            st.markdown(f"**Trend:**")
            st.markdown(f"<span style='color: #FF4B4B;'>{threat['trend']}</span>", 
                        unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"### {threat['threat']}")
            st.markdown(threat['description'])
            
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
    <div>FraudLens Demo v1.0</div>
    <div>© 2025 Your Company</div>
</div>
""", unsafe_allow_html=True)

# Add note that this is a demo
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background-color: #1E2130; padding: 10px; border-radius: 5px; margin-top: 20px;">
    <p style="font-size: 0.8rem; margin: 0;">
        <strong>Demo Note:</strong> This is a demonstration version with simulated data.
        All metrics and visualizations are for illustrative purposes only.
    </p>
</div>
""", unsafe_allow_html=True)