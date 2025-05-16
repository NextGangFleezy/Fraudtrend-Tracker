import pandas as pd
import json
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_custom_fraud_data(file_path="attached_assets/fraud_test_data.json"):
    """
    Load custom fraud data from the provided JSON file.
    
    Parameters:
    -----------
    file_path : str
        Path to the JSON file containing fraud data
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the fraud data with standardized columns
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.warning(f"Custom data file not found: {file_path}")
            return pd.DataFrame()
            
        # Load JSON data
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        logger.info(f"Loaded {len(data)} custom fraud cases from {file_path}")
            
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Standardize column names to match our application schema
        df = standardize_fraud_data(df)
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading custom fraud data: {str(e)}")
        return pd.DataFrame()
        
def standardize_fraud_data(df):
    """
    Standardize the columns in the custom fraud data to match the application schema.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the raw fraud data
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with standardized columns
    """
    # Create a new DataFrame with standardized structure
    standardized_df = pd.DataFrame()
    
    # Map existing columns to our standardized schema
    if not df.empty:
        # Keep case_id as is
        standardized_df['case_id'] = df['case_id'] 
        
        # Convert date to detection_date
        standardized_df['detection_date'] = pd.to_datetime(df['date'])
        
        # Extract fraud type from tags (first tag)
        standardized_df['fraud_type'] = df['tags'].apply(lambda x: x[0].title() if x else "Unknown")
        
        # Set reported amount (not in original data, set to 0)
        standardized_df['reported_amount'] = 0.0
        
        # Map status to risk level
        status_to_risk = {
            'confirmed_fraud': 'High',
            'false_positive': 'Low',
            'under_investigation': 'Medium'
        }
        standardized_df['risk_level'] = df['status'].map(status_to_risk).fillna('Medium')
        
        # Copy status
        standardized_df['status'] = df['status'].map({
            'confirmed_fraud': 'Confirmed',
            'false_positive': 'Closed',
            'under_investigation': 'In Progress'
        }).fillna('Open')
        
        # Set region (not in original data)
        standardized_df['region'] = 'Unknown'
        
        # Map detection method from tags
        tag_to_method = {
            'phishing': 'Customer Report',
            'social engineering': 'Customer Report',
            'account takeover': 'Automated System',
            'carding': 'Fraud Pattern Detection',
            'false positive': 'Manual Review'
        }
        
        def determine_method(tags):
            for tag in tags:
                if tag.lower() in tag_to_method:
                    return tag_to_method[tag.lower()]
            return 'Automated System'
            
        standardized_df['detection_method'] = df['tags'].apply(determine_method)
        
        # Use description as case_summary
        standardized_df['case_summary'] = df['description'] + " " + df['analyst_notes']
        
        # Add columns for tags and analyst_notes (not in original schema)
        standardized_df['tags'] = df['tags'].apply(lambda x: ', '.join(x) if x else '')
        standardized_df['analyst_notes'] = df['analyst_notes']
        
        # Add ID column for database compatibility
        standardized_df['id'] = range(1, len(standardized_df) + 1)
    
    return standardized_df

def merge_with_generated_data(custom_df, generated_df, custom_ratio=0.2):
    """
    Merge custom data with generated data, preserving a specified ratio.
    
    Parameters:
    -----------
    custom_df : pandas.DataFrame
        DataFrame containing the custom fraud data
    generated_df : pandas.DataFrame
        DataFrame containing the generated fraud data
    custom_ratio : float
        Ratio of custom data to include in the final dataset (0.0 to 1.0)
        
    Returns:
    --------
    pandas.DataFrame
        Merged DataFrame
    """
    if custom_df.empty:
        return generated_df
        
    if generated_df.empty:
        return custom_df
        
    # Calculate how many rows to keep from each dataset
    total_rows = len(custom_df) + len(generated_df)
    custom_rows = min(len(custom_df), int(total_rows * custom_ratio))
    generated_rows = total_rows - custom_rows
    
    # Trim datasets to desired sizes
    custom_subset = custom_df.iloc[:custom_rows].copy()
    generated_subset = generated_df.iloc[:generated_rows].copy()
    
    # Ensure case_ids are unique
    generated_subset['case_id'] = [f"GEN-{i:06d}" for i in range(1, len(generated_subset) + 1)]
    
    # Merge datasets
    merged_df = pd.concat([custom_subset, generated_subset], ignore_index=True)
    
    # Reset IDs for database compatibility
    merged_df['id'] = range(1, len(merged_df) + 1)
    
    logger.info(f"Merged {len(custom_subset)} custom cases with {len(generated_subset)} generated cases")
    
    return merged_df