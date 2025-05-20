# Contributing to FraudLens

Thank you for your interest in contributing to FraudLens! Here's how you can help improve this fraud analysis platform.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally: `git clone https://github.com/yourusername/fraudlens.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes to ensure they work as expected
6. Commit your changes: `git commit -m "Add your descriptive commit message"`
7. Push your changes to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request from your fork to the main repository

## Development Environment

To set up your development environment:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .

# Run the application
streamlit run app.py
```

## Code Style

Please follow these guidelines for your code contributions:

- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Include comments for complex logic

## Testing

Before submitting your changes, please make sure to test them thoroughly:

- Test with different data inputs
- Verify visualizations render correctly
- Check for any error conditions

## Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the GitHub issues
2. If not, create a new issue with a clear description and steps to reproduce

## Feature Requests

We welcome suggestions for new features! Please include:

- A clear description of the feature
- The problem it solves
- Any design ideas you have

Thank you for contributing to making FraudLens better!