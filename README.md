# TOPSIS Assignment — CLI Tool, PyPI Package & Web Service

## 📌 Overview

This project implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method in three parts:

- Part 1 — Command-line TOPSIS program  
- Part 2 — Python package published on PyPI  
- Part 3 — Flask-based web service with email result delivery  

TOPSIS is a multi-criteria decision-making method used to rank alternatives based on distance from ideal best and ideal worst solutions.

---

# ✅ Part 1 — Command-Line TOPSIS Program

## Description

A Python script that implements the TOPSIS algorithm and runs from the command line.

## Features

- Accepts input file (CSV / Excel)
- Accepts weights and impacts
- Validates all inputs
- Checks numeric criteria columns
- Handles file-not-found errors
- Generates TOPSIS score and rank
- Outputs result file (CSV)

## Usage
python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>
## Example
python topsis.py data.xlsx "1,1,1,1,1" "+,+,-,+,+" result.csv


## Input Rules

- Minimum 3 columns required
- First column → Alternatives
- Remaining columns → Numeric values only
- Number of weights = number of criteria columns
- Impacts must be `+` or `-`
- Values must be comma-separated

---

# 📦 Part 2 — Python Package (PyPI)

## Description

The TOPSIS program was converted into a reusable Python package and uploaded to PyPI.

## Package Name
Topsis-Akshit-102317084
## PyPI Link
https://pypi.org/project/Topsis-Akshit-102317084/
## Installation

pip install Topsis-Akshit-102317084


## Command-Line Usage After Install

topsis-run <InputFile> <Weights> <Impacts> <OutputFile>


## Example

topsis-run data.xlsx "1,1,1,1,1" "+,+,-,+,+" result.csv


## Package Features

- Console command entry point
- Input validation
- CSV and Excel support
- Rank generation
- PyPI distribution tested after install

---

# 🌐 Part 3 — Web Service (Flask + Email)

## Description

A Flask-based web application that allows users to run TOPSIS through a web interface.

Users can:

- Upload input file
- Enter weights
- Enter impacts
- Enter email address
- Receive result file via email

## Features

- File upload (CSV / Excel)
- Input validation
- Weights & impacts validation
- Email format validation
- Result file sent as email attachment
- Simple HTML interface

---

## How To Run Part 3

### Install Dependencies

pip install flask pandas numpy openpyxl


### Set Email Credentials (Environment Variables)

Linux / Mac:

export TOPSIS_EMAIL="your_email@gmail.com"
export TOPSIS_APP_PASSWORD="your_app_password"


Windows:

set TOPSIS_EMAIL=your_email@gmail.com
set TOPSIS_APP_PASSWORD=your_app_password


### Run Server

python app.py


### Open Browser

http://127.0.0.1:5000/


### Submit Form

- Upload file
- Enter weights (comma-separated)
- Enter impacts (+ / -)
- Enter email ID
- Submit

Result file is sent to the provided email.

---

# 🧮 TOPSIS Methodology

The following steps are implemented:

1. Normalize the decision matrix  
2. Apply weights  
3. Determine ideal best and ideal worst  
4. Compute Euclidean distances  
5. Calculate TOPSIS score  
6. Rank alternatives  

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Flask
- SMTP (Email)
- PyPI Packaging

---

# 👤 Author

**Akshit Singla**  
Roll Number: **102317084**

---

# 📄 License

This project is developed for academic assignment purposes.






