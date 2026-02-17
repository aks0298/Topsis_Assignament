from setuptools import setup, find_packages

setup(
    name="Topsis-Akshit-102317084",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "topsis-run=topsis_akshit.cli:run"
        ]
    },
    author="Akshit",
    description="TOPSIS command line tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
