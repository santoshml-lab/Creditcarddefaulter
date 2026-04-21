

import streamlit as st
import pandas as pd
import joblib

# ---------- CONFIG ----------
st.set_page_config(page_title="Fraud AI", page_icon="💳")

# ---------- LOAD ----------
model = joblib.load("xgb_model.pkl")
cols = joblib.load("columns.pkl")

st.title("💳 Fraud Detection System")
st.markdown("Real-time risk analysis of transactions 🚀")

# ---------- INPUTS ----------
st.subheader("🔍 Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    amt = st.number_input("💰 Amount", min_value=0.0)
    category = st.selectbox("🛒 Category", [
        "shopping_pos","shopping_net","food_dining",
        "gas_transport","grocery_pos","travel"
    ])
    gender = st.selectbox("👤 Gender", ["M","F"])

with col2:
    merchant = st.text_input("🏪 Merchant Name")
    hour = st.slider("🕒 Transaction Hour", 0, 23, 12)
    distance = st.number_input("📍 Distance from Home (km)", min_value=0.0)
    city_pop = st.number_input("🏙 City Population", min_value=0)

# ---------- CREATE DATA ----------
input_dict = {
    "amt": amt,
    "category": category,
    "merchant": merchant,
    "gender": gender,
    "city_pop": city_pop,
    "unix_time": hour * 3600,  # approx
    "distance": distance
}

input_df = pd.DataFrame([input_dict])

# ---------- ENCODING ----------
input_df = pd.get_dummies(input_df)
input_df = input_df.reindex(columns=cols, fill_value=0)

# ---------- PREDICT ----------
if st.button("🚀 Check Risk"):

    prob = model.predict_proba(input_df)[0][1]

    st.subheader("📊 Result")

    st.progress(int(prob * 100))
    st.metric("Fraud Probability", f"{prob:.2f}")

    if prob > 0.6:
        st.error("🚨 High Fraud Risk")
    elif prob > 0.3:
        st.warning("⚠️ Medium Risk")
    else:
        st.success("✅ Safe Transaction")

    # ---------- INSIGHT ----------
    st.write("### 💡 Insight")
    if prob > 0.6:
        st.write("Unusual transaction pattern detected (amount/location/time).")
    else:
        st.write("Transaction aligns with normal behavior patterns.")
