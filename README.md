# FraudLens

![FraudLens Banner](assets/fraud_banner.png)

## A Centralized Fraud Analysis Platform

FraudLens is a powerful tool for fraud investigators that provides a centralized, queryable database of fraud trends with advanced visualization and pattern recognition capabilities.

## Features

- **Real-time Dashboard**: Get instant insights into fraud trends and patterns
- **Case Explorer**: Search similar past cases instantly to inform investigations
- **Pattern Analysis**: Identify emerging fraud patterns using advanced analytics
- **Trend Forecasting**: Predict future fraud trends based on historical data

## Screenshots

![Dashboard](assets/dashboard.png)
![Case Explorer](assets/case_explorer.png)
![Pattern Analysis](assets/pattern_analysis.png)

## Technology Stack

- **Backend**: Python with data processing via Pandas and NumPy
- **Visualization**: Interactive charts with Plotly
- **Frontend**: Streamlit for rapid development of data applications
- **Data Storage**: SQLAlchemy ORM for flexible database connections

## Getting Started

### Prerequisites

- Python 3.8+
- Dependencies listed in requirements.txt

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fraudlens.git
cd fraudlens

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Configuration

The application can connect to a database by setting the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL=postgresql://username:password@localhost:5432/fraud_db
```

If no database is configured, the application will use the sample data provided in `attached_assets/fraud_test_data.json`.

## Project Structure

```
└── FraudLens/
    ├── app.py                  # Main application entry point
    ├── app_basic.py            # Simplified version of the app
    ├── fraudlens_demo.py       # Fully-featured demo version
    ├── assets/                 # Static assets and image utilities
    ├── attached_assets/        # Sample data files
    ├── pages/                  # Multi-page Streamlit application views
    │   ├── case_explorer.py
    │   ├── dashboard.py
    │   ├── pattern_analysis.py
    │   └── trend_analysis.py
    └── utils/                  # Utility functions and modules
        ├── custom_data_loader.py
        ├── data_processing.py
        ├── db_connection.py
        ├── pattern_recognition.py
        ├── sample_data_generator.py
        └── visualization.py
```

## Usage Examples

### Case Search and Analysis

The Case Explorer allows fraud investigators to quickly find similar cases by searching across case details, fraud types, and analyst notes.

### Pattern Recognition

The Pattern Analysis module uses clustering algorithms to identify groups of related fraud cases and surface emerging patterns that might not be immediately obvious.

### Trend Forecasting

Using time-series analysis, FraudLens can predict future fraud trends, helping organizations allocate resources proactively rather than reactively.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- All fraud data used in demos and examples is artificially generated and does not represent real-world cases.
- Icons and images used in the application are from [source].