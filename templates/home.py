import streamlit as st
import pandas as pd

def home_view(usuario, dataset, fecha_filtro):
    st.header("Home")
    st.write(f"Bienvenido al dashboard, {usuario}.")
    st.write(f"Dataset seleccionado: {dataset}")

    try:
        df = pd.read_csv(f'data/{dataset}', delimiter=';', on_bad_lines='skip')
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return
    st.write("Primeras filas del archivo CSV:")
    st.write(df.head())

    columnas_seleccionadas = st.multiselect("Seleccione las columnas", df.columns.tolist())

    if columnas_seleccionadas:
        valores_filtros = {}
        for col in columnas_seleccionadas:
            valor = st.text_input(f"Introduzca valor para la columna {col}")
            if valor:
                valores_filtros[col] = valor

        df_filtrado = df
        for col, valor in valores_filtros.items():
            df_filtrado = df_filtrado[df_filtrado[col].astype(str).str.contains(valor, na=False)]

        cantidad_datos = st.number_input("Cantidad de datos a mostrar", min_value=1, max_value=len(df_filtrado), value=20, step=1)

        st.write(f"Mostrando las primeras {cantidad_datos} filas de los datos filtrados:")
        st.write(df_filtrado.head(cantidad_datos + 1))
    else:
        st.write("Seleccione al menos una columna para filtrar los datos.")
