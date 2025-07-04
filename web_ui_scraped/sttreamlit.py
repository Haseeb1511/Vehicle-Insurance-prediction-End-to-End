# streamlit_app.py

import streamlit as st
import requests

# Set your FastAPI URL
FASTAPI_URL = "http://127.0.0.1:8000/pred"  # change if your FastAPI runs elsewhere

st.set_page_config(page_title="Vehicle Insurance Prediction", page_icon="🚗")

st.title("🚗 Vehicle Insurance Prediction")

st.markdown("Fill the form below to check if a customer is likely to buy vehicle insurance.")

with st.form("prediction_form"):
    Gender = st.selectbox("Gender", ["Male", "Female"])
    Age = st.number_input("Age", min_value=18, max_value=100, value=30)
    Driving_License = st.selectbox("Driving License", [0, 1])
    Region_Code = st.number_input("Region Code", min_value=0.0, value=28.0)
    Previously_Insured = st.selectbox("Previously Insured", ["Yes","No"])
    Annual_Premium = st.number_input("Annual Premium", min_value=0.0, value=30000.0)
    Policy_Sales_Channel = st.number_input("Policy Sales Channel", min_value=0.0, value=26.0)
    Vintage = st.number_input("Vintage", min_value=0, value=100)
    Vehicle_Age_lt_1_Year = st.selectbox("Vehicle Age < 1 Year", [0, 1])
    Vehicle_Age_gt_2_Years = st.selectbox("Vehicle Age > 2 Years", [0, 1])
    Vehicle_Damage_Yes = st.selectbox("Vehicle Damage Yes", ["Yes", "No"])

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "Gender": Gender,
        "Age": Age,
        "Driving_License": Driving_License,
        "Region_Code": Region_Code,
        "Previously_Insured": Previously_Insured,
        "Annual_Premium": Annual_Premium,
        "Policy_Sales_Channel": Policy_Sales_Channel,
        "Vintage": Vintage,
        "Vehicle_Age_lt_1_Year": Vehicle_Age_lt_1_Year,
        "Vehicle_Age_gt_2_Years": Vehicle_Age_gt_2_Years,
        "Vehicle_Damage_Yes": Vehicle_Damage_Yes
    }

    try:
        response = requests.post(FASTAPI_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Prediction: {result['Prediction']}")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"❌ Failed to connect to the prediction API: {e}")
