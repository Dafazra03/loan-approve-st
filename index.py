import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('model/rf_best_model.pkl')

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
        .container {
            background-color: #6DB172;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            width: 60%;
            margin: auto;
        }
        .title {
            color: Blue;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .input-row {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 10px 0;
        }
        .stNumberInput input {
            text-align: center;
            border-radius: 5px;
            height: 40px;
            font-size: 16px;
        }
        .stButton button {
            background-color: #D33F49;
            color: white;
            padding: 10px 30px;
            margin-top: 10px;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #C5303E;
        }
        .result-box {
            margin-top: 20px;
            padding: 20px;
            background-color: #f4f4f4;
            color: black;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
        }
        .icon {
            font-size: 50px;
            margin-bottom: 10px;
        }
        .success {
            color: green;
        }
        .danger {
            color: red;
        }
    </style>
""", unsafe_allow_html=True)

# Judul aplikasi
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

# Mengelompokkan input agar lebih terstruktur
st.subheader("Financial Information")
for col in columns[:5]:
    value = st.number_input(f'{col}', min_value=0.0, value=None, format="%.4f", key=col)
    inputs.append(value)

st.subheader("Loan and Asset Details")
for col in columns[5:]:
    value = st.number_input(f'{col}', min_value=0.0, value=None, format="%.4f", key=col)
    inputs.append(value)

# Fungsi untuk mereset input
def reset_inputs():
    for col in columns:
        st.session_state[col] = None

# Tombol submit dan reset
col1, col2 = st.columns(2)
with col1:
    submit = st.button("Predict")
with col2:
    reset = st.button("Reset", on_click=reset_inputs)

# Validasi jika tombol "Predict" diklik
if submit:
    # Pastikan semua input tidak kosong
    if any(value is None for value in inputs):
        st.warning("⚠️ Semua input harus diisi dengan benar.")
    else:
        df, _ = create_df(inputs)
        st.write('Daftar Input:')
        st.write(df)

        # Prediksi menggunakan model
        prediksi = model.predict(df)
        hasil = "Loan Approved" if prediksi[0] == 1 else "Loan Not Approved"
        icon = "✅" if prediksi[0] == 1 else "❌"
        icon_class = "success" if prediksi[0] == 1 else "danger"

        # Tampilkan hasil prediksi dengan ikon
        st.markdown(f"""
            <div class="result-box">
                <span class="icon {icon_class}">{icon}</span><br>
                {hasil}
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
