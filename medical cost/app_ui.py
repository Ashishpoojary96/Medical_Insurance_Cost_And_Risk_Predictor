import streamlit as st
import pandas as pd
import pickle
import base64

# Load trained model
model = pickle.load(open('rf_model.pkl', 'rb'))

# Set dark theme layout
st.set_page_config(page_title="Insurance Cost Predictor", page_icon="🏥", layout="centered")

# Background image setup
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

encoded_image = get_base64_image("in.avif")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:in/avif;base64,{encoded_image}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# Styling enhancements
st.markdown("""
    <style>
    label, .stSlider, .stSelectbox {
        font-size: 18px !important;
        color: white !important;
        font-weight: bold;
    }
    .css-1xarl3l, .css-q8sbsg {
        font-size: 16px !important;
    }
    .stButton > button {
        font-size: 18px !important;
        padding: 0.75em 1.5em;
        border-radius: 12px;
    }
    .block-container h3 {
        font-size: 22px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Risk classification function
def classify_risk(age, bmi, smoker, children):
    risk_score = 0
    if age > 50:
        risk_score += 2
    elif age > 30:
        risk_score += 1

    if bmi > 30:
        risk_score += 2
    elif bmi > 25:
        risk_score += 1

    if smoker == 'yes':
        risk_score += 3

    if children >= 3:
        risk_score += 1

    if risk_score >= 5:
        return "High Risk"
    elif risk_score >= 3:
        return "Medium Risk"
    else:
        return "Low Risk"

# Title
st.markdown("<h1 style='text-align: center; color: white;'>🏥 Insurance Cost & Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: silver;'>Estimate medical insurance cost and understand your health risk level</p>", unsafe_allow_html=True)

# Personal Info Card
with st.container():
    st.markdown("---")
    st.markdown("""
    <h4 style='color:silver; text-align:center;'>📋 Personal Information</h4>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎂 Age", unsafe_allow_html=True)
        age = st.slider("", 18, 65, 30, key="age_slider")
        st.markdown("#### ⚖️ BMI (Body Mass Index)", unsafe_allow_html=True)
        bmi = st.slider("", 15.0, 40.0, 25.0, step=0.1, key="bmi_slider")
        st.markdown("#### 👶 Number of Children", unsafe_allow_html=True)
        children = st.slider("", 0, 5, 1, key="children_slider")

    with col2:
        st.markdown("#### 🚻 Gender", unsafe_allow_html=True)
        sex = st.selectbox("", ["male", "female"], key="gender_select")
        st.markdown("#### 🚬 Smoker", unsafe_allow_html=True)
        smoker = st.selectbox("", ["yes", "no"], key="smoker_select")
        st.markdown("#### 🌍 Region", unsafe_allow_html=True)
        region = st.selectbox("", ["southeast", "southwest", "northeast", "northwest"], key="region_select")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    predict_button = st.button("🔍 Predict Insurance Cost", use_container_width=True)

# Prediction Logic
if predict_button:
    input_data = {
        'age': age,
        'bmi': bmi,
        'children': children,
        'sex_male': 1 if sex == 'male' else 0,
        'smoker_yes': 1 if smoker == 'yes' else 0,
        'region_northwest': 1 if region == 'northwest' else 0,
        'region_southeast': 1 if region == 'southeast' else 0,
        'region_southwest': 1 if region == 'southwest' else 0
    }

    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    risk_level = classify_risk(age, bmi, smoker, children)

    st.markdown("---")
    st.markdown("### 🎯 Prediction Results")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="💰 Estimated Cost", value=f"${prediction:,.2f}")
    with col2:
        st.metric(label="⚠️ Risk Level", value=risk_level)

    if risk_level == "High Risk":
        st.error("High Risk: Consider consulting a health expert and reviewing your lifestyle.")
    elif risk_level == "Medium Risk":
        st.warning("Medium Risk: Moderate risk. Consider lifestyle adjustments.")
    else:
        st.success("Low Risk: You're at low medical insurance risk. Keep it up! 🎉")

    st.markdown("---")
    st.caption("🔒 This tool is for educational purposes. No personal data is stored.")
