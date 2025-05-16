import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
import os

# Load data function
def load_data():
    """Load fraud test data from JSON file"""
    try:
        with open("attached_assets/fraud_test_data.json", "r") as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Add necessary columns for visualization
        df['detection_date'] = pd.to_datetime(df['date'])
        df['reported_amount'] = 100  # Sample amount for visualization
        df['fraud_type'] = df['tags'].apply(lambda x: x[0].title() if x else "Unknown")
        df['risk_level'] = df['status'].map({
            'confirmed_fraud': 'High',
            'false_positive': 'Low',
            'under_investigation': 'Medium'
        }).fillna('Medium')
        
        # Generate additional test data for better visualization
        additional_data = []
        for i in range(20):
            # Create a variety of dates across several months
            month = (i % 12) + 1
            day = (i % 28) + 1
            record = {
                'case_id': f'GEN-{i:03d}',
                'detection_date': f'2025-{month:02d}-{day:02d}',
                'fraud_type': ['Phishing', 'Carding', 'Social Engineering', 'Account Takeover'][i % 4],
                'reported_amount': (i+1) * 100,
                'risk_level': ['High', 'Medium', 'Low'][i % 3],
                'status': ['Confirmed', 'In Progress', 'Closed'][i % 3],
                'region': ['North America', 'Europe', 'Asia', 'South America'][i % 4],
                'detection_method': ['Customer Report', 'Automated System', 'Manual Review'][i % 3],
                'case_summary': f'Generated test case {i} for visualization purposes'
            }
            additional_data.append(record)
        
        # Combine with the original data
        additional_df = pd.DataFrame(additional_data)
        additional_df['detection_date'] = pd.to_datetime(additional_df['detection_date'])
        combined_df = pd.concat([df, additional_df], ignore_index=True)
        
        return combined_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Create overview chart function
def create_overview_chart(df):
    try:
        # Ensure detection_date is datetime
        df['detection_date'] = pd.to_datetime(df['detection_date'])
        
        # Group by month
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
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        # Return empty chart
        return px.line(title="Fraud Cases Over Time (Error loading data)")

# Create type breakdown chart
def create_fraud_type_chart(df):
    try:
        type_counts = df['fraud_type'].value_counts().reset_index()
        type_counts.columns = ['fraud_type', 'count']
        
        fig = px.bar(
            type_counts,
            x='fraud_type',
            y='count',
            title="Fraud Cases by Type",
            labels={"fraud_type": "Fraud Type", "count": "Number of Cases"}
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return px.bar(title="Fraud Types (Error loading data)")

# Configure page settings
st.set_page_config(
    page_title="FraudLens - Basic Version",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
data = load_data()

# Application header
st.title("FraudLens - Fraud Database Visualizer")
st.subheader("A simplified fraud trend analysis platform")

# Main dashboard overview
st.header("Fraud Trend Overview")

# Display key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Cases", f"{len(data):,}")
with col2:
    st.metric("Avg. Loss Amount", f"${data['reported_amount'].mean():.2f}")
with col3:
    high_risk = len(data[data['risk_level'] == 'High'])
    st.metric("High Risk Cases", f"{high_risk}")
with col4:
    fraud_types = data['fraud_type'].nunique()
    st.metric("Distinct Fraud Types", f"{fraud_types}")

# Display charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_overview_chart(data), use_container_width=True)
    
with col2:
    st.plotly_chart(create_fraud_type_chart(data), use_container_width=True)

# Search functionality
st.header("Search Fraud Cases")
search_query = st.text_input("Search by case ID, fraud type, or keywords")

if search_query:
    # Simple search implementation
    filtered_data = data[
        data['case_id'].str.contains(search_query, case=False, na=False) |
        data['fraud_type'].str.contains(search_query, case=False, na=False) |
        data.get('case_summary', '').str.contains(search_query, case=False, na=False)
    ]
    
    if len(filtered_data) > 0:
        st.write(f"Found {len(filtered_data)} matching cases:")
        st.dataframe(filtered_data)
    else:
        st.info("No matching cases found.")
        
# Display all data
st.header("All Fraud Cases")
st.dataframe(data)

# Footer
st.markdown("---")
st.caption("FraudLens: Improving investigation efficiency through data visualization and pattern recognition")