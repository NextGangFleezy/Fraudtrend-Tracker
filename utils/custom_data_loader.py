import pandas as pd
import json
import os
from datetime import datetime
import logging
import math

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

def _select_row_counts(custom_len, generated_len, custom_ratio):
    """Return the number of custom and generated rows that best match the ratio."""
    if custom_ratio <= 0:
        return 0, generated_len

    if custom_ratio >= 1:
        return custom_len, 0

    total_available = custom_len + generated_len
    if total_available == 0:
        return 0, 0

    # Ensure we always include at least one custom record when custom data exists
    # and a non-zero ratio is requested so the dataset never drops all
    # user-supplied rows.
    min_custom = 1 if custom_len > 0 else 0

    best_key = None
    best_counts = (min_custom if min_custom <= custom_len else 0, 0)

    for total in range(max(1, min_custom), total_available + 1):
        desired_custom = total * custom_ratio
        for target in {math.floor(desired_custom), math.ceil(desired_custom)}:
            custom_rows = target
            if custom_rows < min_custom:
                custom_rows = min_custom
            if custom_rows > custom_len:
                custom_rows = custom_len

            generated_rows = total - custom_rows
            if generated_rows < 0:
                continue

            if generated_rows > generated_len:
                generated_rows = generated_len
                custom_rows = total - generated_rows
                if custom_rows < min_custom or custom_rows > custom_len:
                    continue

            total_used = custom_rows + generated_rows
            if total_used == 0:
                continue

            actual_ratio = custom_rows / total_used
            key = (abs(actual_ratio - custom_ratio), -total_used, -custom_rows)

            if best_key is None or key < best_key:
                best_key = key
                best_counts = (custom_rows, generated_rows)

    if best_key is None:
        if custom_len > 0:
            return min_custom, 0
        if generated_len > 0:
            return 0, min(1, generated_len)
        return 0, 0

    return best_counts


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
        return generated_df.copy()

    if generated_df.empty:
        return custom_df.copy()

    # Clamp the ratio to the valid range to avoid unexpected behaviour
    custom_ratio = max(0.0, min(1.0, custom_ratio))

    if custom_ratio == 0.0:
        merged_df = generated_df.copy()
        merged_df['case_id'] = [f"GEN-{i:06d}" for i in range(1, len(merged_df) + 1)]
        merged_df['id'] = range(1, len(merged_df) + 1)
        logger.info("Custom ratio set to 0. Using only generated data.")
        return merged_df

    if custom_ratio == 1.0:
        merged_df = custom_df.copy()
        merged_df['id'] = range(1, len(merged_df) + 1)
        logger.info("Custom ratio set to 1. Using only custom data.")
        return merged_df

    custom_rows, generated_rows = _select_row_counts(
        len(custom_df), len(generated_df), custom_ratio
    )

    custom_subset = custom_df.iloc[:custom_rows].copy()
    generated_subset = generated_df.iloc[:generated_rows].copy()

    # Ensure case_ids are unique
    generated_subset['case_id'] = [f"GEN-{i:06d}" for i in range(1, len(generated_subset) + 1)]

    # Merge datasets
    merged_df = pd.concat([custom_subset, generated_subset], ignore_index=True)

    # Reset IDs for database compatibility
    merged_df['id'] = range(1, len(merged_df) + 1)

    total_rows = len(custom_subset) + len(generated_subset)
    actual_ratio = (len(custom_subset) / total_rows) if total_rows > 0 else 0

    logger.info(
        "Merged %s custom cases with %s generated cases (actual ratio %.3f)",
        len(custom_subset),
        len(generated_subset),
        actual_ratio,
    )

    return merged_df
