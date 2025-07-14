# FraudLens Project Documentation

## Project Overview
FraudLens is a centralized fraud analysis platform that empowers fraud investigators to search similar past cases instantly, identify evolving fraud patterns, improve decision-making accuracy, and shorten investigation cycles to meet SLA targets.

**Technology Stack:**
- Frontend: Streamlit interactive web application
- Data Processing: Pandas, NumPy for data manipulation
- Visualization: Plotly for interactive charts
- Machine Learning: Scikit-learn for pattern recognition
- Database: SQLAlchemy ORM with PostgreSQL support
- Architecture: Multi-page modular design

## Current State
- ✅ Full production application (app.py) is running
- ✅ Multi-page navigation with Dashboard, Case Explorer, Pattern Analysis, and Trend Analysis
- ✅ Complete database integration capabilities with fallback to sample data
- ✅ Advanced visualization suite with interactive charts
- ✅ Machine learning pattern recognition and anomaly detection
- ✅ Comprehensive documentation package (README, LinkedIn post, technical architecture)
- ✅ Professional project structure ready for GitHub/portfolio sharing

## Recent Changes (January 2025)
- **2025-01-14**: Created comprehensive README.md with detailed documentation including:
  - Complete feature overview and business benefits
  - Installation and setup instructions
  - Project architecture documentation
  - Usage guide for all major features
  - Development and contribution guidelines
  - Security, performance, and scalability considerations
- **Previous**: Reverted from demo version back to full production application
- **Previous**: Integrated custom fraud test data with generated sample data
- **Previous**: Created complete GitHub-ready documentation suite

## Project Architecture
- **Main Application**: `app.py` - Full-featured fraud analysis platform
- **Pages Module**: Multi-page Streamlit application structure
  - Dashboard: Interactive fraud trend visualization
  - Case Explorer: Search and case similarity matching
  - Pattern Analysis: ML-powered clustering and anomaly detection
  - Trend Analysis: Time-series forecasting and predictions
- **Utils Module**: Core utility functions for data processing, visualization, and ML
- **Data Integration**: Supports PostgreSQL database or falls back to JSON sample data
- **Assets**: Image utilities and sample fraud case data

## User Preferences
- Prefers full production version over demo/simplified versions
- Values comprehensive documentation for professional presentation
- Wants GitHub-ready project structure for portfolio sharing
- Requires working application with all advanced features enabled

## Development Notes
- Application runs on port 5000 via Streamlit
- Uses environment variable DATABASE_URL for database connection
- Falls back to attached_assets/fraud_test_data.json when no database configured
- All fraud data is artificially generated for demonstration purposes
- Project includes professional licensing, contribution guidelines, and setup instructions