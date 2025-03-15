import streamlit as st
import pandas as pd
import joblib

model = joblib.load('model/rf_new.pkl')

st.title('Input Angka dengan Streamlit')

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

st.write('Masukkan 10 angka:')

# Dapatkan kolom dari fungsi create_df
_, columns = create_df([0] * 10)

for i, col in enumerate(columns):
    value = st.number_input(f'{col}', min_value=0.0, value=0.0, format="%.4f")
    inputs.append(value)

# Tombol submit
if st.button('Submit'):
    df, _ = create_df(inputs)
    st.write('Daftar Input:')
    st.write(df)

    # Arahkan data ke model Anda
    prediksi = model.predict(df)

    if prediksi[0] == 0:
        res = "Not Approve"
    else:
        res = "Approve"

    st.write(f'Hasil Prediksi: {res}')
