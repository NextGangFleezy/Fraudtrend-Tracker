import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create SQLAlchemy Base
Base = declarative_base()

# Define Fraud Case model
class FraudCase(Base):
    __tablename__ = 'fraud_cases'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(String(50), unique=True, nullable=False)
    detection_date = Column(Date, nullable=False)
    fraud_type = Column(String(100), nullable=False)
    reported_amount = Column(Float)
    risk_level = Column(String(20))
    status = Column(String(20))
    region = Column(String(100))
    detection_method = Column(String(100))
    case_summary = Column(Text)
    
# Database connection function
def get_database_connection():
    """
    Create a connection to the database using environment variables.
    Returns SQLAlchemy engine.
    """
    try:
        # Try to get database URL from environment variable
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            logger.warning("No DATABASE_URL environment variable found")
            # Display a message in the Streamlit UI if we're in a Streamlit app
            if 'db_connection_error' not in st.session_state:
                st.session_state.db_connection_error = True
            return None
            
        # Create SQLAlchemy engine
        engine = create_engine(database_url)
        logger.info("Database connection established")
        return engine
        
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        if 'db_connection_error' not in st.session_state:
            st.session_state.db_connection_error = True
        return None

def init_database():
    """
    Initialize the database by creating all tables defined in the models.
    """
    engine = get_database_connection()
    if engine:
        try:
            # Create tables
            Base.metadata.create_all(engine)
            logger.info("Database tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            return False
    return False

def get_session():
    """
    Create a database session.
    """
    engine = get_database_connection()
    if engine:
        Session = sessionmaker(bind=engine)
        return Session()
    return None

# Convert SQLAlchemy models to pandas DataFrame
def query_to_dataframe(query_results):
    """
    Convert SQLAlchemy query results to pandas DataFrame.
    """
    if not query_results:
        return pd.DataFrame()
        
    # Extract data as dictionaries
    data = [row.__dict__ for row in query_results]
    
    # Remove SQLAlchemy state instance
    for row in data:
        if '_sa_instance_state' in row:
            del row['_sa_instance_state']
            
    # Convert to DataFrame
    return pd.DataFrame(data)