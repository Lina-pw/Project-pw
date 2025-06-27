import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import zscore

st.title("Calculadora de Retención Semanal")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV (separado por ';')", type=["csv"])

# Nombre del archivo de salida
output_filename = st.text_input("Nombre del archivo de salida (sin .xlsx)", value="retencion_resultado")

if uploaded_file and output_filename:
    # Leer archivo
    df = pd.read_csv(uploaded_file, sep=';')
    df_backup = df.copy()

    st.subheader("Vista previa del archivo cargado")
    st.dataframe(df.head())

    # Detectar la primera columna automáticamente como semana base
    columna_actual = df.columns[0]
    cuentas_activas = set(df[columna_actual].dropna())

    # Calcular retención
    retencion_corrigida = {}
    for col in df.columns:
        if col != columna_actual:
            cuentas_anteriores = set(df[col].dropna())
            retencion_corrigida[col] = len(cuentas_anteriores & cuentas_activas)

    # Crear DataFrame con resultados
    df_retencion_corrigida = pd.DataFrame(list(retencion_corrigida.items()),
                                          columns=["Semana", "Cuentas Retenidas"])

    # Invertir el orden
    df_invertido = df_retencion_corrigida.iloc[::-1].reset_index(drop=True)

    st.subheader("Resultado de retención calculada")
    st.dataframe(df_invertido)

    # Guardar como Excel
    output_path = f"{output_filename}.xlsx"
    df_invertido.to_excel(output_path, index=False)

    st.success(f"Archivo generado: {output_path}")
    with open(output_path, "rb") as f:
        st.download_button("Descargar archivo Excel",
                           data=f,
                           file_name=output_path,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
