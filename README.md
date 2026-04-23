
![Python](https://img.shields.io/badge/Python-3.10-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-XGBoost-orange)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

💳 Credit Card Fraud Detection System
🚀 A full-stack machine learning system that detects fraudulent transactions in real-time using data-driven risk scoring.
🔥 Live Demo
🌐 API: 

🧠 Problem Statement
Credit card fraud is a major financial risk. Traditional rule-based systems fail to adapt to evolving fraud patterns.
This project builds a machine learning-powered fraud detection system that:
Learns from historical transaction data
Detects suspicious patterns
Provides risk-based predictions in real-time

⚙️ System Architecture
User Input → Streamlit UI → FastAPI Backend → ML Model → Prediction → UI Display
🚀 Features
✔ Real-time fraud prediction
✔ Probability-based risk scoring (LOW / MEDIUM / HIGH)
✔ Distance-based anomaly detection
✔ Clean fintech-style dashboard
✔ Explainable insights (rule-based + model-driven)
✔ Deployed API + UI
🧪 Sample Output

Amount
Distance
Probability
Risk
₹100
0.01
0.003
LOW
₹15000
60+
0.65
HIGH

🧠 Machine Learning Approach
Model: XGBoost Classifier
Feature Engineering:
Distance between user & merchant
Transaction category encoding
Population-based context
Imbalance Handling:
scale_pos_weight tuning

📊 Key Insight
“Fraud detection is not based on a single rule, but on a combination of risk signals.”
The model captures:
High-value transactions
Unusual geographic distance
Risk-prone categories
Contextual population patterns

🖥️ Tech Stack
Python
FastAPI
Streamlit
XGBoost
Pandas / NumPy
📦 Installation
pip install -r requirements.txt
▶️ Run Locally
Start API
uvicorn app:app --reload
Run UI
streamlit run app_ui.py
⚠️ Disclaimer
This is a demo system built for educational and portfolio purposes.
Real-world fraud systems use more complex data and large-scale pipelines.
👨‍💻 Author
Santosh
Aspiring Machine Learning Engineer 🚀
⭐ If you like this project
Give it a ⭐ on GitHub and share feedback!


