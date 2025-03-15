import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('model/rf_new.pkl')

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
        .container {
            background-color: #6DB172;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }
        .title {
            color: white;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .input-box {
            margin: 5px;
            padding: 8px;
            border-radius: 5px;
            width: 100%;
            text-align: center;
        }
        .submit-button {
            background-color: #D33F49;
            color: white;
            padding: 10px 30px;
            margin-top: 20px;
            border-radius: 5px;
            font-weight: bold;
        }
        .result-box {
            margin-top: 20px;
            padding: 15px;
            background-color: white;
            color: black;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Judul aplikasi
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="title">Credit Risk Prediction</div>', unsafe_allow_html=True)

# Fungsi untuk membuat DataFrame
def create_df(inps):
    columns = [
        "RiskScore", "MonthlyIncome", "TotalDebtToIncomeRatio",
        "AnnualIncome", "InterestRate", "LoanAmount",
        "BaseInterestRate", "NetWorth", "TotalAssets", "MonthlyLoanPayment"
    ]
    jeson = {col: [val] for col, val in zip(columns, inps)}
    df = pd.DataFrame(jeson)
    return df, columns

inputs = []

# Ambil nama kolom dari fungsi
_, columns = create_df([0] * 10)

# Input angka
for i, col in enumerate(columns):
    value = st.number_input(f'{col}', min_value=0.0, value=0.0, format="%.4f", key=f'input_{i}')
    inputs.append(value)

# Tombol submit
if st.button('Enter', key='submit', help='Klik untuk memprediksi', css_class="submit-button"):
    df, _ = create_df(inputs)
    st.write('Daftar Input:')
    st.write(df)

    # Prediksi menggunakan model
    prediksi = model.predict(df)
    hasil = "Loan Approved" if prediksi[0] == 1 else "Loan Not Approved"

    # Tampilkan hasil prediksi
    st.markdown(f'<div class="result-box">{hasil}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
