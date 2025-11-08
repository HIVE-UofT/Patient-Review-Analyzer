"""
Setup configuration for the theme categorization package.
"""
from setuptools import setup, find_packages

setup(
    name="theme_categorization",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai>=1.0.0",
        "pandas>=1.3.0",
        "tqdm>=4.65.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
) 