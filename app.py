import streamlit as st
import requests
import math
import plotly.graph_objects as go

API_URL = "https://defaulter-credit-5.onrender.com/predict"

st.set_page_config(page_title="Fraud Risk Dashboard", layout="wide")

# ---------- MAP FUNCTION ----------
def show_map(lat, long, merch_lat, merch_long, risk):

    color = "green" if risk == "LOW" else "orange" if risk == "MEDIUM" else "red"

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=[lat],
        lon=[long],
        mode='markers',
        marker=dict(size=12, color='blue'),
        name="User"
    ))

    fig.add_trace(go.Scattermapbox(
        lat=[merch_lat],
        lon=[merch_long],
        mode='markers',
        marker=dict(size=12, color=color),
        name="Merchant"
    ))

    fig.add_trace(go.Scattermapbox(
        lat=[lat, merch_lat],
        lon=[long, merch_long],
        mode='lines',
        line=dict(width=2, color=color),
        name="Transaction Path"
    ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=(lat+merch_lat)/2, lon=(long+merch_long)/2),
            zoom=2
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- HEADER ----------
st.title("💳 Fraud Detection Intelligence System")
st.markdown("Real-time ML-powered transaction risk analysis 🚀")

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

    lat = st.number_input("User Latitude", value=28.6)
    long = st.number_input("User Longitude", value=77.2)
    merch_lat = st.number_input("Merchant Latitude", value=28.61)
    merch_long = st.number_input("Merchant Longitude", value=77.21)

    run = st.button("🔍 Analyze Transaction")

# ---------- DISTANCE ----------
distance = math.sqrt((lat-merch_lat)**2 + (long-merch_long)**2)

# ---------- API CALL ----------
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

        # ---------- METRICS ----------
        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Amount", f"₹{amt}")
        col2.metric("📏 Distance", f"{distance:.2f}")
        col3.metric("📊 Probability", f"{prob:.2f}")

        st.markdown("---")

        # ---------- RISK ----------
        if risk == "HIGH":
            st.error("🚨 HIGH FRAUD RISK DETECTED")
        elif risk == "MEDIUM":
            st.warning("⚠️ MEDIUM RISK TRANSACTION")
        else:
            st.success("✅ LOW RISK TRANSACTION")

        # ---------- INSIGHTS ----------
        st.subheader("🧠 Risk Insights")

        reasons = []

        if amt > 10000:
            reasons.append("💰 High transaction amount")

        if distance > 20:
            reasons.append("📍 Large distance between user and merchant")

        if city_pop < 1000 and amt > 3000:
            reasons.append("🏙️ Small city high-value transaction")

        if category in ["shopping_pos", "misc_pos"] and amt > 3000:
            reasons.append("🛒 Risk-prone category with high spend")

        if len(reasons) == 0:
            st.write("No major risk signals detected.")
        else:
            for r in reasons:
                st.write("•", r)

        # ---------- SUMMARY ----------
        st.markdown("---")
        st.subheader("📌 Summary")

        st.info(f"""
        Category: {category}  
        Gender: {gender}  
        City Population: {city_pop}  

        👉 Probability: {prob:.2f}  
        👉 Risk Level: **{risk}**
        """)

        # ---------- MAP ----------
        st.markdown("---")
        st.subheader("🗺️ Transaction Map")

        show_map(lat, long, merch_lat, merch_long, risk)

    else:
        st.error("❌ API Error")
