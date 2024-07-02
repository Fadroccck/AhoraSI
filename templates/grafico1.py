import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos(ruta):
    return pd.read_csv(ruta, delimiter=';')

def grafico1_view(dataset, fecha_filtro):
    df = cargar_datos(f'data/{dataset}')
    st.write("Vista de Gráfico 1")
    st.write(df.head())
