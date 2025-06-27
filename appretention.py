import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import zscore

st.title("Conversor de CSV a Excel con Análisis Básico")

uploaded_file = st.file_uploader("Sube tu archivo CSV (separado por ';')", type=["csv"])
output_filename = st.text_input("Nombre del archivo de salida (sin extensión)", value="salida")

if uploaded_file and output_filename:
    df = pd.read_csv(uploaded_file, sep=';')
    df_backup = df.copy()

    st.subheader("Vista previa del archivo cargado")
    st.dataframe(df.head())

    # (Opcional) Análisis mínimo - por ejemplo, aplicar z-score
    try:
        numeric_df = df.select_dtypes(include=[np.number])
        z_scores = zscore(numeric_df)
        df_z = pd.DataFrame(z_scores, columns=numeric_df.columns)
        st.subheader("Z-Scores (columnas numéricas)")
        st.dataframe(df_z.head())
    except Exception as e:
        st.warning(f"No se pudo calcular Z-Score: {e}")

    output_path = f"{output_filename}.xlsx"
    df.to_excel(output_path, index=False)

    st.success(f"Archivo generado: {output_path}")
    with open(output_path, "rb") as f:
        st.download_button(
            "Descargar archivo Excel",
            data=f,
            file_name=output_path,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
