import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import zscore

st.title("Calcule Retention UP Excel")

# Subida del archivo Excel
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

# Nombre del archivo de salida
output_filename = st.text_input("Nombre del archivo de salida (sin .xlsx)", value="retention_result")

if uploaded_file and output_filename:
    # Leer Excel
    df = pd.read_excel(uploaded_file)
    df_backup = df.copy()

    st.subheader("Vista previa del archivo cargado")
    st.dataframe(df.head())

    # Usar la primera columna como semana base
    columna_actual = df.columns[0]
    cuentas_activas = set(df[columna_actual].dropna())

    retencion_corrigida = {}
    for col in df.columns:
        if col != columna_actual:
            cuentas_anteriores = set(df[col].dropna())
            retencion_corrigida[col] = len(cuentas_anteriores & cuentas_activas)

    df_retencion_corrigida = pd.DataFrame(list(retencion_corrigida.items()),
                                          columns=["Semana", "Cuentas Retenidas"])
    df_invertido = df_retencion_corrigida.iloc[::-1].reset_index(drop=True)

    st.subheader("Resultado de retención calculada")
    st.dataframe(df_invertido)

    # Exportar como Excel
    output_path = f"{output_filename}.xlsx"
    df_invertido.to_excel(output_path, index=False)

    st.success(f"Archivo generado: {output_path}")
    with open(output_path, "rb") as f:
        st.download_button("Descargar archivo Excel",
                           data=f,
                           file_name=output_path,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
