import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Patient Vital Signs Monitoring System")

# Normal ranges
NORMAL_RANGES = {
    "Heart Rate": (60, 100),
    "Systolic BP": (90, 120),
    "Diastolic BP": (60, 80),
    "Temperature": (36.1, 37.2),
    "SpO2": (95, 100)
}

# Function to predict condition
def predict_condition(hr, temp, spo2, sys_bp, dia_bp):

    conditions = []

    if hr > 100:
        conditions.append("Possible Tachycardia")
    elif hr < 60:
        conditions.append("Possible Bradycardia")

    if temp > 37.5:
        conditions.append("Possible Fever / Infection")

    if spo2 < 95:
        conditions.append("Possible Respiratory Problem")

    if sys_bp > 130 or dia_bp > 85:
        conditions.append("Possible Hypertension")

    if sys_bp < 90 or dia_bp < 60:
        conditions.append("Possible Hypotension")

    if len(conditions) == 0:
        return "Healthy / Normal"

    return ", ".join(conditions)


st.header("Enter Patient Data")

name = st.text_input("Patient Name")
age = st.number_input("Age", 0, 120)

hr = st.number_input("Heart Rate (bpm)")
sys_bp = st.number_input("Systolic BP (mmHg)")
dia_bp = st.number_input("Diastolic BP (mmHg)")
temp = st.number_input("Temperature (°C)")
spo2 = st.number_input("SpO2 (%)")

if st.button("Analyze Patient"):

    condition = predict_condition(hr, temp, spo2, sys_bp, dia_bp)

    st.subheader("Predicted Health Condition")
    st.write(condition)

    data = {
        "Name": name,
        "Age": age,
        "Heart Rate": hr,
        "Systolic BP": sys_bp,
        "Diastolic BP": dia_bp,
        "Temperature": temp,
        "SpO2": spo2,
        "Condition": condition
    }

    df = pd.DataFrame([data])

    st.subheader("Patient Record")
    st.write(df)

    df.to_csv("patient_vital_signs.csv", mode='a', header=False, index=False)

    st.success("Patient data saved")

    # -------- GRAPHS --------

    st.subheader("Heart Rate Trend")

    fig1, ax1 = plt.subplots()
    ax1.plot(df["Heart Rate"], marker='o')
    ax1.set_title("Heart Rate Trend")
    st.pyplot(fig1)

    st.subheader("Temperature Comparison")

    fig2, ax2 = plt.subplots()
    sns.barplot(x=df["Name"], y=df["Temperature"], ax=ax2)
    st.pyplot(fig2)

    st.subheader("SpO2 Comparison")

    fig3, ax3 = plt.subplots()
    sns.barplot(x=df["Name"], y=df["SpO2"], ax=ax3)
    st.pyplot(fig3)

    st.subheader("Blood Pressure Distribution")

    fig4, ax4 = plt.subplots()
    ax4.scatter(df["Systolic BP"], df["Diastolic BP"])
    ax4.set_xlabel("Systolic BP")
    ax4.set_ylabel("Diastolic BP")
    st.pyplot(fig4)