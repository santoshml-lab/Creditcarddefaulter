
import streamlit as st
import requests
import math

API_URL = "https://defaulter-credit-5.onrender.com/predict"

st.set_page_config(page_title="Fraud Risk Dashboard", layout="wide")

# ---------- HEADER ----------
st.title("💳 Fraud Risk Dashboard")
st.markdown("Smart fraud detection powered by ML 🚀")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("🧾 Transaction Input")

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

    st.markdown("---")

    # 🎯 DEMO BUTTONS
    if st.button("🟢 Normal Example"):
        amt, category, gender, city_pop = 120, "grocery_pos", "F", 50000
        lat, long, merch_lat, merch_long = 28.6, 77.2, 28.61, 77.21

    if st.button("🔴 Fraud Example"):
        amt, category, gender, city_pop = 15000, "shopping_pos", "M", 500
        lat, long, merch_lat, merch_long = 28.6, 77.2, 40.7, -74.0

    run = st.button("🔍 Analyze")

# ---------- HELPER ----------
def calc_distance(lat, long, mlat, mlong):
    return math.sqrt((lat-mlat)**2 + (long-mlong)**2)

# ---------- MAIN ----------
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

        # ---------- METRICS ----------
        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Amount", f"₹{amt}")
        col2.metric("📏 Distance", f"{distance:.2f}")
        col3.metric("📊 Probability", f"{prob:.2f}")

        st.markdown("---")

        # ---------- RISK BANNER ----------
        if risk == "HIGH":
            st.error("🚨 HIGH FRAUD RISK — Immediate Attention Needed")
        elif risk == "MEDIUM":
            st.warning("⚠️ MEDIUM RISK — Review Recommended")
        else:
            st.success("✅ LOW RISK — Looks Safe")

        # ---------- INSIGHTS ----------
        st.subheader("🧠 Why this result?")

        reasons = []

        if distance > 20:
            reasons.append("📍 Transaction location is far from user location")

        if amt > 5000:
            reasons.append("💰 High transaction amount detected")

        if city_pop < 1000:
            reasons.append("🏙️ Small population area — unusual behavior")

        if category in ["shopping_pos", "misc_pos"]:
            reasons.append("🛒 Risk-prone transaction category")

        if len(reasons) == 0:
            st.write("No major risk signals detected")
        else:
            for r in reasons:
                st.write(f"- {r}")

        # ---------- SUMMARY ----------
        st.markdown("---")
        st.subheader("📌 Summary")

        st.info(f"""
        **Category:** {category}  
        **Gender:** {gender}  
        **City Population:** {city_pop}  

        👉 **Fraud Probability:** {prob:.2f}  
        👉 **Final Risk Level:** **{risk}**
        """)

    else:
        st.error("❌ API Error — backend issue")
