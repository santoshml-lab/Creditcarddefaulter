import streamlit as st
import pandas as pd
import joblib

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Fraud AI", page_icon="💳", layout="centered")

# ---------- LOAD MODEL ----------
model = joblib.load("xgb_model.pkl")
cols = joblib.load("columns.pkl")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
}
.sub-text {
    text-align: center;
    color: grey;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="big-title">💳 Fraud Detection AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Smart system to detect risky transactions 🚀</div>', unsafe_allow_html=True)

st.write("")

# ---------- INPUT CARD ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🔍 Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    amt = st.number_input("💰 Amount", min_value=0.0)
    gender = st.selectbox("👤 Gender", ["M", "F"])

with col2:
    category = st.selectbox("🛒 Category", ["shopping", "food", "travel"])
    city_pop = st.number_input("🏙 City Population", min_value=0)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- CREATE INPUT ----------
input_dict = {
    "amt": amt,
    "gender": gender,
    "category": category,
    "city_pop": city_pop
}

input_df = pd.DataFrame([input_dict])

# ---------- ENCODING ----------
input_df = pd.get_dummies(input_df)
input_df = input_df.reindex(columns=cols, fill_value=0)

# ---------- BUTTON ----------
if st.button("🚀 Check Fraud Risk"):

    prob = model.predict_proba(input_df)[0][1]

    st.write("")
    st.subheader("📊 Result")

    # ---------- RISK BAR ----------
    st.progress(int(prob * 100))

    st.metric("Fraud Probability", f"{prob:.2f}")

    # ---------- DECISION ----------
    if prob > 0.5:
        st.error("🚨 High Fraud Risk")
    elif prob > 0.3:
        st.warning("⚠️ Medium Risk")
    else:
        st.success("✅ Safe Transaction")

    # ---------- EXTRA INSIGHT ----------
    st.write("### 💡 Insight")
    if prob > 0.5:
        st.write("Transaction shows strong fraud patterns. Immediate review recommended.")
    else:
        st.write("Transaction appears normal based on learned patterns.")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using Machine Learning")
