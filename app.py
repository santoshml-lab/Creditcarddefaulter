
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ---------- CONFIG ----------
st.set_page_config(page_title="FinGuard AI", page_icon="🛡️", layout="centered")

# ---------- LOAD ----------
model = joblib.load("xgb_model.pkl")
cols = joblib.load("columns.pkl")

# ---------- HEADER ----------
st.title("🛡️ FinGuard AI - Fraud Detection System")
st.caption("AI-powered real-time transaction risk analysis")

st.write("---")

# ---------- INPUT ----------
st.subheader("Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    amt = st.number_input("💰 Transaction Amount", min_value=0.0)
    category = st.selectbox("🛒 Category", [
        "shopping_net","shopping_pos","food_dining",
        "gas_transport","grocery_pos","travel"
    ])
    gender = st.selectbox("👤 Gender", ["M","F"])

with col2:
    merchant = st.text_input("🏪 Merchant Name")
    city_pop = st.number_input("🏙 City Population", min_value=0)
    distance = st.number_input("📍 Distance from Home (km)", min_value=0.0)

st.write("---")

# ---------- PREPROCESS ----------
input_dict = {
    "amt": amt,
    "category": category,
    "gender": gender,
    "merchant": merchant,
    "city_pop": city_pop,
    "distance": distance
}

df = pd.DataFrame([input_dict])
df = pd.get_dummies(df)
df = df.reindex(columns=cols, fill_value=0)

# ---------- PREDICTION ----------
if st.button("🔍 Analyze Risk"):

    prob = model.predict_proba(df)[0][1]
    risk_percent = prob * 100

    st.subheader("📊 Risk Analysis Result")

    # ---------- GAUGE METER ----------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percent,
        title={'text': "Fraud Risk Level (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------- DECISION ----------
    if prob > 0.6:
        st.error("🚨 HIGH RISK: Fraud Likely Detected")
        st.write("Immediate verification recommended.")
    elif prob > 0.3:
        st.warning("⚠️ MEDIUM RISK: Suspicious Activity")
        st.write("Manual review suggested.")
    else:
        st.success("✅ LOW RISK: Transaction Safe")

    st.write("---")
    st.caption("Powered by XGBoost + Behavioral Pattern Analysis")
