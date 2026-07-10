Student Performance Analytics Dashboard
Objective

The objective of this project is to perform Exploratory Data Analysis (EDA) on a student performance dataset and develop an interactive dashboard using Streamlit to uncover patterns, trends, and relationships affecting academic performance.

Dataset Description

The dataset contains information about students including:

Gender
Absence Days
Weekly Self Study Hours
Career Aspirations
Part-Time Job Status
Subject Scores
Student Information

Total Records: 2000+

Data Cleaning Process

The following preprocessing steps were performed:

Handled missing values
Removed duplicate records
Calculated average score
Detected and removed outliers using IQR
Prepared dataset for analysis
EDA Methodology

The following analyses were conducted:

Statistical Summary
Distribution Analysis
Correlation Analysis
Trend Analysis
Feature Relationship Analysis
Key Insights
Students with higher self-study hours tend to achieve better academic performance.
Higher absence days negatively affect academic outcomes.
Subject scores are positively correlated.
Career aspirations vary significantly among students.
Part-time jobs have limited impact on performance.
Technologies Used
Python
Pandas
NumPy
Streamlit
Plotly
Matplotlib
Seaborn
Installation Guide
pip install -r requirements.txt
Run the Dashboard
streamlit run app.py
Dashboard Screenshots

GitHub Repository:

