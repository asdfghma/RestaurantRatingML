import streamlit as st
import numpy as np
import joblib

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Restaurant Rating Predictor",
    layout="wide",
    page_icon="🍽️"
)

# ---------- CUSTOM CSS ----------
custom_css = """
<style>
/* Background image with dark overlay */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                      url("https://images.unsplash.com/photo-1504674900247-0877df9cc836");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Transparent header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Main container */
.block-container {
    background-color: rgba(255, 255, 255, 0.08);
    padding: 2rem;
    border-radius: 15px;
}

/* Input fields */
.stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #000 !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    border-radius: 6px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}

/* Labels */
label {
    color: #E9ECEF !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Title */
h1 {
    font-size: 44px !important;
    font-weight: 800 !important;
    color: #FFFFFF  !important; 
    text-align: center;
}

/* Caption */
.stCaption {
    color: #CED4DA !important;
    font-size: 18px !important;
    font-weight: 500 !important;
    text-align: center;
}

/* Prediction box */
.prediction-box {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 250px;           
    height: 60px;           
    margin: 10px auto;      
    border-radius: 10px;
    font-size: 18px;        
    font-weight: 600;
    color: white;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.3);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- LOAD MODEL & SCALER ----------
scaler = joblib.load("Scaler.pkl")
model = joblib.load("mlmodel.pkl")

# ---------- TITLE ----------
st.markdown("<h1>🍽️ Restaurant Rating Prediction</h1>", unsafe_allow_html=True)
st.caption("Predict a restaurant's review score and class based on given features.")

st.divider()

# ---------- INPUT FORM ----------
col1, col2 = st.columns(2)

with col1:
    averagecost = st.number_input(
        "💰 Estimated average cost for two",
        min_value=50,
        max_value=9999999,
        value=1000,
        step=200
    )

    pricenrange = st.selectbox(
        "📊 Price range (1 = Cheapest, 4 = Most Expensive)",
        [1, 2, 3, 4]
    )

with col2:
    tablebooking = st.selectbox(
        "📅 Table booking available?",
        ["Yes", "No"]
    )

    onlinedelivery = st.selectbox(
        "📦 Online delivery available?",
        ["Yes", "No"]
    )

st.divider()

# ---------- PREDICTION ----------
predictbutton = st.button("🔮 Predict Review", use_container_width=True)

if predictbutton:
    bookingstatus = 1 if tablebooking == "Yes" else 0
    deliverystatus = 1 if onlinedelivery == "Yes" else 0

    values = [[averagecost, bookingstatus, deliverystatus, pricenrange]]
    X = scaler.transform(np.array(values))

    prediction = model.predict(X)[0]

    st.markdown(
        f"<div class='prediction-box' style='background-color:#444;'>Predicted Score: {prediction:.2f}</div>",
        unsafe_allow_html=True
    )

    if prediction < 2.5:
        result = "😞 Poor"
        color = "#DC3545"  
    elif prediction < 3.5:
        result = "😐 Average"
        color = "#FFC107"  
    elif prediction < 4.0:
        result = "🙂 Good"
        color = "#0DCAF0"  
    elif prediction < 4.5:
        result = "😃 Very Good"
        color = "#198754"  
    else:
        result = "🤩 Excellent"
        color = "#6610F2"  

    st.markdown(
        f"<div class='prediction-box' style='background-color:{color};'>{result}</div>",
        unsafe_allow_html=True
    )