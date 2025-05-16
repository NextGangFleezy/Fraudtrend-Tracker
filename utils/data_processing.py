import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import logging
import os
import streamlit as st
from sqlalchemy import text, func, or_
from utils.db_connection import get_database_connection, get_session, FraudCase, query_to_dataframe, init_database

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data loading and processing functions

def load_data():
    """
    Load fraud data from the database.
    If no database connection is available, returns sample test data.
    """
    try:
        # Get database session
        session = get_session()
        
        if not session:
            logger.info("Database connection not available. Using sample test data.")
            # Generate sample test data instead of an empty DataFrame
            return generate_test_data(200)  # Generate 200 test records
        
        # Query all fraud cases
        cases = session.query(FraudCase).all()
        
        # Convert to DataFrame
        df = query_to_dataframe(cases)
        
        # Close session
        session.close()
        
        # If we got no data from database, use sample data
        if df.empty:
            logger.info("No data found in database. Using sample test data.")
            return generate_test_data(200)  # Generate 200 test records
            
        return df
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        st.error(f"Error loading data: {str(e)}")
        # Return test data as a fallback
        return generate_test_data(200)

def generate_test_data(num_records=100):
    """
    Generate sample test data for the FraudLens application.
    This provides realistic-looking fraud data for testing and demonstration.
    """
    # Define lists of possible values for categorical fields
    fraud_types = [
        "Identity Theft", "Payment Fraud", "Account Takeover", 
        "Synthetic Identity", "Wire Fraud", "Loan Fraud",
        "Credit Card Fraud", "Check Fraud", "Money Laundering"
    ]
    
    risk_levels = ["Low", "Medium", "High", "Critical"]
    
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    
    regions = [
        "North America", "Europe", "Asia Pacific", 
        "Latin America", "Middle East", "Africa"
    ]
    
    detection_methods = [
        "Automated System", "Manual Review", "Customer Report", 
        "Fraud Pattern Detection", "Transaction Monitoring", 
        "AI/ML Detection", "External Tip"
    ]
    
    # Generate random dates within the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # Approximately 2 years
    
    # Create empty DataFrame to store the data
    df = pd.DataFrame()
    
    # Generate case IDs
    df['case_id'] = [f"CASE-{i:06d}" for i in range(1, num_records + 1)]
    
    # Generate detection dates
    random_days = np.random.randint(0, 730, size=num_records)
    df['detection_date'] = [end_date - timedelta(days=int(days)) for days in random_days]
    
    # Generate fraud types
    df['fraud_type'] = np.random.choice(fraud_types, size=num_records)
    
    # Generate reported amounts (using a log-normal distribution for realistic fraud amounts)
    mean_amount = 10000  # Mean fraud amount in currency units
    df['reported_amount'] = np.random.lognormal(
        mean=np.log(mean_amount), 
        sigma=1.2, 
        size=num_records
    ).round(2)
    
    # Generate risk levels (weighted to have more medium/high cases)
    risk_weights = [0.2, 0.4, 0.3, 0.1]  # Low, Medium, High, Critical
    df['risk_level'] = np.random.choice(risk_levels, p=risk_weights, size=num_records)
    
    # Generate statuses (weighted to have more open/in progress cases)
    status_weights = [0.4, 0.3, 0.2, 0.1]  # Open, In Progress, Resolved, Closed
    df['status'] = np.random.choice(statuses, p=status_weights, size=num_records)
    
    # Generate regions
    df['region'] = np.random.choice(regions, size=num_records)
    
    # Generate detection methods
    df['detection_method'] = np.random.choice(detection_methods, size=num_records)
    
    # Generate case summaries
    summary_templates = [
        "Suspicious {fraud_type} detected on {date} in {region}. Amount: ${amount}. Risk: {risk}.",
        "Potential {fraud_type} identified through {method} in {region}. Amount involved: ${amount}.",
        "{method} flagged possible {fraud_type} on {date}. Region: {region}. Amount: ${amount}.",
        "Customer reported {fraud_type} incident in {region}. Transaction amount: ${amount}.",
        "{fraud_type} alert triggered by {method}. Amount: ${amount}. Risk level: {risk}."
    ]
    
    # Generate case summaries for each row
    case_summaries = []
    for i, row in df.iterrows():
        template = random.choice(summary_templates)
        summary = template.format(
            fraud_type=row['fraud_type'].lower(),
            date=row['detection_date'].strftime('%Y-%m-%d'),
            region=row['region'],
            amount=f"{row['reported_amount']:,.2f}",
            method=row['detection_method'].lower(),
            risk=row['risk_level'].lower()
        )
        case_summaries.append(summary)
    
    df['case_summary'] = case_summaries
    
    # Add dummy ID column for consistency with database schema
    df['id'] = range(1, len(df) + 1)
    
    logger.info(f"Generated {len(df)} sample test records")
    return df

def search_fraud_data(df, query, filters=None):
    """
    Search the fraud database for matching cases based on query and filters
    Returns filtered dataframe of matching records
    """
    try:
        # Check if we have a direct database connection
        session = get_session()
        
        if session:
            # Use SQLAlchemy to query the database directly
            search_query = session.query(FraudCase)
            
            # Apply text search if query is provided
            if query and query.strip():
                search_terms = [f"%{term}%" for term in query.split()]
                search_conditions = []
                
                for term in search_terms:
                    search_conditions.append(or_(
                        FraudCase.case_id.ilike(term),
                        FraudCase.fraud_type.ilike(term),
                        FraudCase.region.ilike(term),
                        FraudCase.detection_method.ilike(term),
                        FraudCase.case_summary.ilike(term)
                    ))
                
                if search_conditions:
                    search_query = search_query.filter(or_(*search_conditions))
            
            # Apply filters if provided
            if filters:
                if filters.get('fraud_type'):
                    search_query = search_query.filter(FraudCase.fraud_type.in_(filters['fraud_type']))
                
                if filters.get('risk_level'):
                    search_query = search_query.filter(FraudCase.risk_level.in_(filters['risk_level']))
                
                if filters.get('date_range') and all(filters['date_range']):
                    start_date, end_date = filters['date_range']
                    search_query = search_query.filter(
                        FraudCase.detection_date.between(start_date, end_date)
                    )
                
                if filters.get('amount_range') and all(filters['amount_range']):
                    min_amount, max_amount = filters['amount_range']
                    search_query = search_query.filter(
                        FraudCase.reported_amount.between(min_amount, max_amount)
                    )
            
            # Execute query
            results = search_query.all()
            
            # Convert to DataFrame
            result_df = query_to_dataframe(results)
            
            # Close session
            session.close()
            
            return result_df
        
        # Fallback to pandas filtering if no direct database connection
        if df.empty:
            return df
            
        filtered_df = df.copy()
        
        # Apply text search
        if query and not filtered_df.empty:
            query = query.lower()
            mask = filtered_df['case_id'].str.lower().str.contains(query, na=False)
            mask |= filtered_df['fraud_type'].str.lower().str.contains(query, na=False)
            mask |= filtered_df['region'].str.lower().str.contains(query, na=False)
            mask |= filtered_df['detection_method'].str.lower().str.contains(query, na=False)
            mask |= filtered_df['case_summary'].str.lower().str.contains(query, na=False)
            filtered_df = filtered_df[mask]
        
        # Apply additional filters
        if filters and not filtered_df.empty:
            if filters.get('fraud_type'):
                filtered_df = filtered_df[filtered_df['fraud_type'].isin(filters['fraud_type'])]
            
            if filters.get('risk_level'):
                filtered_df = filtered_df[filtered_df['risk_level'].isin(filters['risk_level'])]
            
            if filters.get('date_range') and all(filters['date_range']):
                start_date, end_date = filters['date_range']
                filtered_df = filtered_df[
                    (filtered_df['detection_date'] >= start_date) & 
                    (filtered_df['detection_date'] <= end_date)
                ]
            
            if filters.get('amount_range') and all(filters['amount_range']):
                min_amount, max_amount = filters['amount_range']
                filtered_df = filtered_df[
                    (filtered_df['reported_amount'] >= min_amount) & 
                    (filtered_df['reported_amount'] <= max_amount)
                ]
        
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error searching data: {str(e)}")
        st.error(f"Error searching data: {str(e)}")
        return pd.DataFrame()

def calculate_similarity(case_id1, case_id2, df):
    """
    Calculate similarity between two fraud cases
    """
    if df.empty or case_id1 not in df['case_id'].values or case_id2 not in df['case_id'].values:
        return 0.0
        
    # Get case data
    case1 = df[df['case_id'] == case_id1].iloc[0]
    case2 = df[df['case_id'] == case_id2].iloc[0]
    
    # Calculate similarity based on fraud type, amount, risk level, and region
    similarity = 0.0
    
    # Add similarity for matching fraud types (30% weight)
    if case1['fraud_type'] == case2['fraud_type']:
        similarity += 0.3
    
    # Add similarity for region (20% weight)
    if case1['region'] == case2['region']:
        similarity += 0.2
    
    # Add similarity for detection method (15% weight)
    if case1['detection_method'] == case2['detection_method']:
        similarity += 0.15
    
    # Add similarity for risk level (15% weight)
    if case1['risk_level'] == case2['risk_level']:
        similarity += 0.15
    
    # Add similarity for reported amount (20% weight)
    # If both amounts exist, calculate similarity based on relative difference
    if pd.notna(case1['reported_amount']) and pd.notna(case2['reported_amount']):
        amount1 = case1['reported_amount']
        amount2 = case2['reported_amount']
        
        if amount1 == 0 and amount2 == 0:
            similarity += 0.2
        else:
            # Calculate relative difference
            max_amount = max(amount1, amount2)
            if max_amount > 0:
                diff = abs(amount1 - amount2) / max_amount
                # Convert difference to similarity (1.0 - diff), capped at 0.2
                amount_similarity = max(0, min(1.0 - diff, 1.0)) * 0.2
                similarity += amount_similarity
    
    return similarity

def prepare_time_series_data(df, time_unit='month'):
    """
    Prepare time series data for trend analysis
    """
    if df.empty:
        return pd.DataFrame()
    
    # Make sure detection_date is datetime type
    df['detection_date'] = pd.to_datetime(df['detection_date'])
    
    # Set time grouping based on time_unit
    if time_unit.lower() == 'day':
        df['time_group'] = df['detection_date'].dt.date
    elif time_unit.lower() == 'week':
        df['time_group'] = df['detection_date'].dt.to_period('W').dt.start_time
    elif time_unit.lower() == 'month':
        df['time_group'] = df['detection_date'].dt.to_period('M').dt.start_time
    elif time_unit.lower() == 'quarter':
        df['time_group'] = df['detection_date'].dt.to_period('Q').dt.start_time
    elif time_unit.lower() == 'year':
        df['time_group'] = df['detection_date'].dt.to_period('Y').dt.start_time
    
    # Group data by the time unit
    time_series = df.groupby('time_group').agg({
        'case_id': 'count',
        'reported_amount': ['sum', 'mean', 'median']
    }).reset_index()
    
    # Flatten the column names
    time_series.columns = ['time_period', 'count', 'amount_sum', 'amount_mean', 'amount_median']
    
    return time_series

def get_case_details(case_id, df):
    """
    Get detailed information about a specific case
    """
    if df.empty or case_id not in df['case_id'].values:
        return {}
    
    # Get case data
    case = df[df['case_id'] == case_id].iloc[0].to_dict()
    
    # Try to get from database directly if available
    session = get_session()
    if session:
        db_case = session.query(FraudCase).filter(FraudCase.case_id == case_id).first()
        if db_case:
            # Convert to dict
            case = {c.name: getattr(db_case, c.name) for c in db_case.__table__.columns}
        session.close()
    
    return case

def export_data(df, format='csv'):
    """
    Export data to various formats
    """
    if df.empty:
        return None
        
    if format.lower() == 'csv':
        return df.to_csv(index=False)
    elif format.lower() == 'excel':
        # In a real app, this would return an Excel file
        # For now, we'll use CSV as a fallback
        return df.to_csv(index=False)
    elif format.lower() == 'json':
        return df.to_json(orient='records')
    return None

def filter_fraud_data(df, filters):
    """
    Apply filters to the fraud data
    """
    if df.empty or not filters:
        return df
    
    filtered_df = df.copy()
    
    # Apply filters
    if filters.get('fraud_type'):
        filtered_df = filtered_df[filtered_df['fraud_type'].isin(filters['fraud_type'])]
    
    if filters.get('risk_level'):
        filtered_df = filtered_df[filtered_df['risk_level'].isin(filters['risk_level'])]
    
    if filters.get('date_range') and all(filters['date_range']):
        filtered_df['detection_date'] = pd.to_datetime(filtered_df['detection_date'])
        start_date, end_date = pd.to_datetime(filters['date_range'][0]), pd.to_datetime(filters['date_range'][1])
        filtered_df = filtered_df[
            (filtered_df['detection_date'] >= start_date) & 
            (filtered_df['detection_date'] <= end_date)
        ]
    
    if filters.get('amount_range') and all([x is not None for x in filters['amount_range']]):
        min_amount, max_amount = filters['amount_range']
        filtered_df = filtered_df[
            (filtered_df['reported_amount'] >= min_amount) & 
            (filtered_df['reported_amount'] <= max_amount)
        ]
    
    if filters.get('region'):
        filtered_df = filtered_df[filtered_df['region'].isin(filters['region'])]
    
    if filters.get('status'):
        filtered_df = filtered_df[filtered_df['status'].isin(filters['status'])]
    
    return filtered_df

# Alias for backward compatibility
load_sample_data = load_data
