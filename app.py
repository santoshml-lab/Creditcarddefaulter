import streamlit as st
import requests
import math

API_URL = "https://defaulter-credit-5.onrender.com/predict"

st.set_page_config(page_title="Fraud Risk Dashboard", layout="wide")

# ---------- HEADER ----------
st.title("💳 Fraud Risk Dashboard")
st.caption("Real-time risk scoring for transactions")

# ---------- INPUTS ----------
with st.sidebar:
    st.header("🧾 Transaction Inputs")

    amt = st.number_input("💰 Amount", min_value=0.0, value=100.0)
    category = st.selectbox("🛒 Category", [
        "food_dining","gas_transport","grocery_net","grocery_pos",
        "health_fitness","home","kids_pets","misc_net","misc_pos",
        "personal_care","shopping_net","shopping_pos","travel"
    ])
    gender = st.selectbox("👤 Gender", ["M","F"])
    city_pop = st.number_input("🏙️ City Population", min_value=1, value=50000)

    st.markdown("---")
    st.subheader("📍 Location")

    lat = st.number_input("Your Latitude", value=28.6)
    long = st.number_input("Your Longitude", value=77.2)
    merch_lat = st.number_input("Merchant Latitude", value=28.61)
    merch_long = st.number_input("Merchant Longitude", value=77.21)

    run = st.button("🔍 Analyze")

# ---------- HELPER ----------
def calc_distance(lat, long, mlat, mlong):
    return math.sqrt((lat-mlat)**2 + (long-mlong)**2)

# ---------- MAIN DASHBOARD ----------
if run:
    data = {
        "amt": amt,
        "category": category,
        "gender": gender,
        "city_pop": city_pop,
        "lat": lat,
        "long": long,
        "merch_lat": merch_lat,
        "merch_long": merch_long
    }

    res = requests.post(API_URL, json=data)

    if res.status_code == 200:
        result = res.json()
        prob = result["probability"]
        risk = result["risk"]

        distance = calc_distance(lat, long, merch_lat, merch_long)

        # ---------- TOP METRICS ----------
        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Amount", f"₹{amt}")
        col2.metric("📏 Distance", f"{distance:.2f}")
        col3.metric("📊 Probability", f"{prob:.2f}")

        st.markdown("---")

        # ---------- RISK STATUS ----------
        if risk == "HIGH":
            st.error("🚨 HIGH FRAUD RISK")
        elif risk == "MEDIUM":
            st.warning("⚠️ MEDIUM FRAUD RISK")
        else:
            st.success("✅ LOW FRAUD RISK")

        # ---------- INSIGHTS ----------
        st.subheader("🧠 Insights")

        if distance > 20:
            st.write("📍 Unusual location detected (far transaction)")
        if amt > 5000:
            st.write("💰 High transaction amount")
        if city_pop < 1000:
            st.write("🏙️ Small city — unusual pattern")

        # ---------- SUMMARY CARD ----------
        st.markdown("---")
        st.subheader("📌 Summary")

        st.info(f"""
        Transaction Category: {category}  
        Gender: {gender}  
        City Population: {city_pop}  

        👉 Model Confidence: {prob:.2f}  
        👉 Final Risk Level: **{risk}**
        """)

    else:
        st.error("❌ API Error — check backend")
