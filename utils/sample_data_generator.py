import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging
from sqlalchemy import text
from utils.db_connection import get_session, get_database_connection, FraudCase, init_database

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sample_fraud_data(num_records=100):
    """
    Generate sample fraud data for testing and development.
    In a production environment, this would be replaced by real data from various sources.
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
    df['detection_date'] = [
        start_date + (end_date - start_date) * random.random()
        for _ in range(num_records)
    ]
    
    # Generate fraud types
    df['fraud_type'] = [random.choice(fraud_types) for _ in range(num_records)]
    
    # Generate reported amounts (using a log-normal distribution for realistic fraud amounts)
    mean_amount = 10000  # Mean fraud amount in currency units
    df['reported_amount'] = np.random.lognormal(
        mean=np.log(mean_amount), 
        sigma=1.2, 
        size=num_records
    ).round(2)
    
    # Generate risk levels (weighted to have more medium/high cases)
    risk_weights = [0.2, 0.4, 0.3, 0.1]  # Low, Medium, High, Critical
    df['risk_level'] = [
        np.random.choice(risk_levels, p=risk_weights)
        for _ in range(num_records)
    ]
    
    # Generate statuses (weighted to have more open/in progress cases)
    status_weights = [0.4, 0.3, 0.2, 0.1]  # Open, In Progress, Resolved, Closed
    df['status'] = [
        np.random.choice(statuses, p=status_weights)
        for _ in range(num_records)
    ]
    
    # Generate regions
    df['region'] = [random.choice(regions) for _ in range(num_records)]
    
    # Generate detection methods
    df['detection_method'] = [random.choice(detection_methods) for _ in range(num_records)]
    
    # Generate case summaries
    summary_templates = [
        "Suspicious {fraud_type} detected on {date} in {region}. Amount: ${amount}. Risk: {risk}.",
        "Potential {fraud_type} identified through {method} in {region}. Amount involved: ${amount}.",
        "{method} flagged possible {fraud_type} on {date}. Region: {region}. Amount: ${amount}.",
        "Customer reported {fraud_type} incident in {region}. Transaction amount: ${amount}.",
        "{fraud_type} alert triggered by {method}. Amount: ${amount}. Risk level: {risk}."
    ]
    
    df['case_summary'] = [
        random.choice(summary_templates).format(
            fraud_type=row['fraud_type'].lower(),
            date=row['detection_date'].strftime('%Y-%m-%d'),
            region=row['region'],
            amount=f"{row['reported_amount']:,.2f}",
            method=row['detection_method'].lower(),
            risk=row['risk_level'].lower()
        )
        for _, row in df.iterrows()
    ]
    
    return df

def load_sample_data_to_database(num_records=100):
    """
    Generate sample data and load it into the database.
    
    Returns:
    --------
    bool
        True if data was successfully loaded, False otherwise
    """
    try:
        # Initialize database tables
        if not init_database():
            logger.error("Failed to initialize database")
            return False
        
        # Generate sample data
        df = generate_sample_fraud_data(num_records)
        
        # Get database session
        session = get_session()
        if not session:
            logger.error("Failed to get database session")
            return False
        
        # Check if there's already data in the database
        existing_count = session.query(FraudCase).count()
        
        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} fraud cases. Skipping data generation.")
            session.close()
            return True
        
        # Convert DataFrame to list of FraudCase objects
        fraud_cases = []
        for _, row in df.iterrows():
            fraud_case = FraudCase(
                case_id=row['case_id'],
                detection_date=row['detection_date'].date(),
                fraud_type=row['fraud_type'],
                reported_amount=float(row['reported_amount']),
                risk_level=row['risk_level'],
                status=row['status'],
                region=row['region'],
                detection_method=row['detection_method'],
                case_summary=row['case_summary']
            )
            fraud_cases.append(fraud_case)
        
        # Add all fraud cases to the database
        session.add_all(fraud_cases)
        session.commit()
        
        logger.info(f"Successfully loaded {len(fraud_cases)} sample fraud cases into the database")
        session.close()
        return True
        
    except Exception as e:
        logger.error(f"Error loading sample data to database: {str(e)}")
        return False

if __name__ == "__main__":
    # When run directly, generate and load sample data
    load_sample_data_to_database(100)