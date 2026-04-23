
![Python](https://img.shields.io/badge/Python-3.10-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-XGBoost-orange)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)


💳 Credit Card Fraud Detection System (ML + API + Dashboard)

🚀 Project Overview
Field
Detail
🎯 Goal
Detect fraudulent credit card transactions
🧠 Type
Machine Learning Classification System
⚙️ Output
LOW / MEDIUM / HIGH Risk
🌐 Deployment
FastAPI + Streamlit
📊 Model
XGBoost Classifier

🔗 Live Links
Component
Link
🌐 API
https://defaulter-credit-5.onrender.com/
📊 Dashboard 
https://creditcarddefaulter-iptgn6vyth4zfg6uqcitto.streamlit.app/



🧠 ML Pipeline
Step
Description
1️⃣ Data Cleaning
Removed irrelevant columns
2️⃣ Feature Engineering
Distance between user & merchant
3️⃣ Encoding
One-hot encoding for categorical data
4️⃣ Model
XGBoost Classifier
5️⃣ Handling Imbalance
scale_pos_weight tuning
6️⃣ Output
Probability + Risk Level

📊 Features Used
Feature
Type
Description
amt
Numeric
Transaction amount
category
Categorical
Transaction type
gender
Categorical
User gender
city_pop
Numeric
Population of city
distance
Numeric

📉 Risk Logic
Probability Range
Risk Level
0.00 – 0.10
LOW
0.10 – 0.40
MEDIUM
0.40 – 1.00
HIGH

🧪 Sample Predictions
Amount
Distance
Probability
Risk
₹120
0.01
0.003
LOW
₹5000
15.2
0.27
MEDIUM
₹15000
60.0
0.65
HIGH

⚙️ Tech Stack
Layer
Tools
Backend
FastAPI
Frontend
Streamlit
ML Model
XGBoost
Data Processing
Pandas, NumPy
Deployment
Render + Streamlit Cloud

🧠 Key Insights
Insight
Meaning
Distance high + Amount high
High fraud risk
Small city + large transaction
Suspicious pattern
Category risk
Shopping/Misc categories more sensitive

Installation
pip install -r requirements.txt

▶️ Run Project
Start API
uvicorn app:app --reload
Start UI
streamlit run app_ui.py

👨‍💻 Author
Name
Detail
Developer
Santosh
Role
ML + Backend + UI Builder
⭐ If you like this project, star it on GitHub 🚀



