from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fraudlens",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A centralized fraud analysis platform with visualization capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fraudlens",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.25.0",
        "pandas>=1.5.0",
        "numpy>=1.22.0",
        "plotly>=5.10.0",
        "scikit-learn>=1.0.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
    ],
)