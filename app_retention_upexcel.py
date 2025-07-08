import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import zscore

st.title("Calculate Retention - UP Excel")

# Excel file upload
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])
st.caption("🔁 The columns must be arranged from left to right, from the most recent week to the oldest.")

# Output file name
output_filename = st.text_input("Output file name (without .xlsx)", value="retention_result")
st.caption(" 📊 This function calculates how many accounts from column A (the most recent week) are repeated in each of the other weeks. The result will be sorted from top to bottom, from the oldest to the most recent week.")

if uploaded_file and output_filename:
    # Read Excel
    df = pd.read_excel(uploaded_file)
    df_backup = df.copy()

    st.subheader("Preview of uploaded file")
    st.dataframe(df.head())

    # Use the first column as the base week
    current_column = df.columns[0]
    active_accounts = set(df[current_column].dropna())

    corrected_retention = {}
    for col in df.columns:
        if col != current_column:
            previous_accounts = set(df[col].dropna())
            corrected_retention[col] = len(previous_accounts & active_accounts)

    df_corrected_retention = pd.DataFrame(list(corrected_retention.items()),
                                          columns=["Week", "Retained Accounts"])
    df_inverted = df_corrected_retention.iloc[::-1].reset_index(drop=True)

    st.subheader("Retention Calculation Result")
    st.dataframe(df_inverted)

    # Export to Excel
    output_path = f"{output_filename}.xlsx"
    df_inverted.to_excel(output_path, index=False)

    st.success(f"File generated: {output_path}")
    with open(output_path, "rb") as f:
        st.download_button("Download Excel File",
                           data=f,
                           file_name=output_path,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
