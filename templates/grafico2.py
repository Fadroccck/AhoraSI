import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos(ruta):
    return pd.read_csv(ruta, delimiter=';')

def grafico2_view(dataset, fecha_filtro):
    df = cargar_datos(f'data/{dataset}')
    st.write("Vista de Gráfico 2")
    st.bar_chart(df[['Aerolinea Nombre', 'Pasajeros']].groupby('Aerolinea Nombre').sum())
