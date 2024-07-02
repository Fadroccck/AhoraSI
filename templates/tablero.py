import streamlit as st
from streamlit_elements import elements, mui, dashboard
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

@st.cache_data
def cargar_datos(ruta):
    return pd.read_csv(ruta, delimiter=';')

def crear_graficos(df):
    tabla1 = df.head()
    grafico2 = df.groupby('Aerolinea Nombre')['Pasajeros'].sum().reset_index()
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    options = {
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
        ],
    }

    return tabla1, grafico2, chart_data, options

def tablero_view(dataset, fecha_filtro):
    df = cargar_datos(f'data/{dataset}')
    tabla1, grafico2, chart_data, options = crear_graficos(df)

    layout = [
        dashboard.Item("grafico_1", 0, 0, 6, 3),
        dashboard.Item("grafico_2", 6, 0, 6, 3),
        dashboard.Item("grafico_3", 0, 3, 6, 3),
        dashboard.Item("grafico_4", 6, 3, 6, 3),
    ]

    with elements("dashboard"):
        with dashboard.Grid(layout):
            with mui.Paper(key="grafico_1", elevation=3):
                with st.container():
                    st.write("Tabla: Primeros 5 datos")
                    st.dataframe(tabla1)

            with mui.Paper(key="grafico_2", elevation=3):
                with st.container():
                    st.write("Gráfico de Barras")
                    st.bar_chart(data=grafico2, x='Aerolinea Nombre', y='Pasajeros')

            with mui.Paper(key="grafico_3", elevation=3):
                with st.container():
                    st.write("Gráfico de Líneas")
                    st.line_chart(chart_data)

            with mui.Paper(key="grafico_4", elevation=3):
                with st.container():
                    st.write("Gráfico de Echarts")
                    st_echarts(options=options)

if __name__ == "__main__":
    tablero_view()
