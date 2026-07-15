import pandas as pd
import numpy as np
import streamlit as st
import pickle

@st.cache_resource #file will not reload again 

#taking load fn for loading file files 
def load():
    with open(r"model.pkl", "rb") as file: #load model file
        model = pickle.load(file)
    with open(r"scaler.pkl", "rb") as file: #load scaler file
        scaler = pickle.load(file)
        return model, scaler
    
model, scaler = load() #calling fn on both variables

#page layout
st.title("Loan Approvel System") #writting title 
st.write("Welcome To The Loan Approval System") #display text

col1, col2 = st.columns(2) #taking cols for seperation of numbers and text inputs

with col1: #numrical inputs
    no_of_dependents = st.number_input("no of departments?", value=None, min_value=0)
    income_annum = st.number_input("income annum?", value=None, min_value=0)
    loan_amount = st.number_input("loan amount?", value=None, min_value=0)
    loan_term = st.number_input("loan term?", value=None, min_value=0)
    cibil_score = st.number_input("cibil score?", value=None, min_value=0)
    residential_assets_value = st.number_input("residential assets value?", value=None, min_value=0)
    commercial_assets_value = st.number_input("commercial assets value?", value=None, min_value=0)
    luxury_assets_value = st.number_input("luxury assets value?", value=None, min_value=0)
    bank_asset_value = st.number_input("bank asset value?", value=None, min_value=0)

with col2: #text inputs
    education = st.selectbox('education', [' Graduate', ' Not Graduate'], index=None)
    self_employed = st.selectbox('self employed', [' Yes', ' No'], index=None)

#puting prediction button
if st.button("click for check"):

#prediction processing after taking inputs 
    input = {
     ' no_of_dependents': no_of_dependents,
     ' income_annum': income_annum,
     ' loan_amount': loan_amount,
     ' loan_term': loan_term,
     ' cibil_score': cibil_score,
     ' residential_assets_value': residential_assets_value,
     ' commercial_assets_value': commercial_assets_value,
     ' luxury_assets_value': luxury_assets_value,
     ' bank_asset_value': bank_asset_value,

    #assign key values to education selectionbox options and put condition on it
     ' education_ Graduate': 1 if education == ' Graduate' else 0,
     ' education_ Not Graduate': 1 if education == ' Not Graduate' else 0,

    #assign key values to self employed selectionbox options and put condition on it
     ' self_employed_ No': 1 if self_employed == ' No' else 0,
     ' self_employed_ Yes': 1 if self_employed == ' Yes' else 0,
    }

    #make data frame of input dic in which user input data stored 
    input_data = pd.DataFrame([input])

    #scale the data frame 
    scaled_data = scaler.transform(input_data)

    #prediction on scaled data 
    prediction = model.predict(scaled_data)

    #display the prediction value
    if prediction == 1:
       st.success(f"Loan Accepted")
    else:
       rejection_reasons = []
       if cibil_score < 700:
            rejection_reasons.append(f"Low CIBIL Score ({cibil_score}). A score of 700+ is generally required.")

       if loan_amount > (income_annum * 3):
            rejection_reasons.append("Requested loan amount is too high compared to your annual income.")

       total_assets = residential_assets_value + commercial_assets_value + luxury_assets_value + bank_asset_value
       if total_assets < loan_amount:
            rejection_reasons.append("Insufficient total amount of asset for requested loan amount.")

       st.error("Loan Rejected")