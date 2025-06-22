import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open("model/model.pkl","rb") as f:
    model = pickle.load(f)


st.title("Vehicle Insurance Prediction")
st.set_page_config(page_icon="🚙",
                   layout="wide")
                   
with st.form("user_form"):
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    driving_license = st.selectbox("Driving License", [0, 1])
    region_code = st.number_input("Region Code", value=28.0)
    previously_insured = st.selectbox("Previously Insured", [0, 1])
    vehicle_age = st.selectbox("Vehicle Age", ["< 1 Year", "1-2 Year", "> 2 Years"])
    vehicle_damage = st.selectbox("Vehicle Damage", ["Yes", "No"])
    annual_premium = st.number_input("Annual Premium", value=30000.0)
    policy_sales_channel = st.number_input("Policy Sales Channel", value=152.0)
    vintage = st.number_input("Vintage", value=150)

    submitted = st.form_submit_button("Predict")


user_input = pd.DataFrame([{
    "gender": "Male",
    "age": 35,
    "driving_license": 1,
    "region_code": 28.0,
    "previously_insured": 0,
    "vehicle_age": "< 1 Year",
    "vehicle_damage": "Yes",
    "annual_premium": 30000.0,
    "policy_sales_channel": 152.0,
    "vintage": 150
}])
    
def preprocessing_function(data:pd.DataFrame)->pd.DataFrame:
    data["gender"] = data["gender"].map({"Male": 0, "Female": 1})
    data["vehicle_damage"] = data["vehicle_damage"].astype("int")
    return data
    
if submitted:
    preprocessing_function(user_input)


# st.success(f"Prediction: {'Interested in Insurance' if prediction == 1 else 'Not Interested'}")