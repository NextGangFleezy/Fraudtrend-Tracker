import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st

def create_overview_chart(df):
    """
    Create an overview line chart of fraud cases over time
    Uses actual data from the dataset
    """
    try:
        if df is not None and not df.empty and 'detection_date' in df.columns:
            # Make sure detection_date is datetime type
            df['detection_date'] = pd.to_datetime(df['detection_date'])
            
            # Group by month and count cases
            df_copy = df.copy()
            df_copy['month'] = df_copy['detection_date'].dt.strftime('%Y-%m')
            monthly_counts = df_copy.groupby('month').size().reset_index(name='count')
            
            # Create the figure
            fig = px.line(
                monthly_counts, 
                x='month', 
                y='count',
                markers=True,
                title="Fraud Cases Over Time",
                labels={"month": "Date", "count": "Number of Cases"}
            )
            
            # Update layout
            fig.update_layout(
                template="plotly_dark",
                height=400,
                margin=dict(l=40, r=40, t=40, b=40),
                hovermode="x unified"
            )
            
            return fig
        else:
            # Create empty figure
            fig = px.line(
                x=[],
                y=[],
                title="Fraud Cases Over Time",
                labels={"x": "Date", "y": "Number of Cases"}
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400,
                margin=dict(l=40, r=40, t=40, b=40),
                annotations=[{
                    "text": "Visualization will appear when data is loaded",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                    "font": {"size": 14}
                }]
            )
            
            return fig
    except Exception as e:
        # If there's an error, show an empty chart with an error message
        fig = px.line(
            x=[],
            y=[],
            title="Fraud Cases Over Time",
            labels={"x": "Date", "y": "Number of Cases"}
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            annotations=[{
                "text": f"Error creating visualization",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 14, "color": "red"}
            }]
        )
        
        return fig

def create_fraud_type_chart(df):
    """
    Create a bar chart of fraud cases by type
    """
    # Create empty figure
    fig = go.Figure()
    
    # Set layout
    fig.update_layout(
        title="Fraud Cases by Type",
        xaxis_title="Fraud Type",
        yaxis_title="Number of Cases",
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    try:
        if df is not None and not df.empty and 'fraud_type' in df.columns:
            # Count cases by fraud type
            type_counts = df['fraud_type'].value_counts().reset_index()
            type_counts.columns = ['fraud_type', 'count']
            
            # Sort by count descending
            type_counts = type_counts.sort_values('count', ascending=False)
            
            # Add bar chart
            fig.add_trace(
                go.Bar(
                    x=type_counts['fraud_type'],
                    y=type_counts['count'],
                    marker_color='#4F8BF9'
                )
            )
            
            # Update layout for better readability
            fig.update_layout(
                xaxis=dict(tickangle=45)
            )
        else:
            # Add annotation if no data
            fig.add_annotation(
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                text="Visualization will appear when data is loaded",
                showarrow=False,
                font=dict(size=14)
            )
    except Exception as e:
        # Add error annotation
        fig.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text="Error creating visualization",
            showarrow=False,
            font=dict(size=14, color="red")
        )
    
    return fig

def create_heatmap(df, x_col, y_col, z_col):
    """
    Create a heatmap visualization
    """
    # Create empty figure
    fig = go.Figure()
    
    # Set layout
    fig.update_layout(
        title=f"Heatmap of {z_col} by {x_col} and {y_col}",
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    # Add annotation
    fig.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig

def create_geographic_map(df):
    """
    Create a geographic map of fraud cases
    """
    # Create empty figure
    fig = go.Figure()
    
    # Set layout
    fig.update_layout(
        title="Geographic Distribution of Fraud Cases",
        template="plotly_dark",
        height=600,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    # Add annotation
    fig.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig

def create_similarity_network(df, case_id=None):
    """
    Create a network visualization of case similarities
    """
    # Create empty figure
    fig = go.Figure()
    
    # Set layout
    fig.update_layout(
        title="Case Similarity Network",
        template="plotly_dark",
        height=600,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    # Add annotation
    fig.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig

def create_trend_forecast(df, forecast_periods=12):
    """
    Create a time series forecast visualization
    """
    # Create empty figure
    fig = go.Figure()
    
    # Set layout
    fig.update_layout(
        title="Fraud Trend Forecast",
        xaxis_title="Date",
        yaxis_title="Number of Cases",
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    
    # Add annotation
    fig.add_annotation(
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        text="Visualization will appear when data is loaded",
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig
