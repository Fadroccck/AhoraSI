import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from login import login, logout

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

if not st.session_state["logged_in"]:
    login()
else:
    st.set_page_config(page_title="Dashboard")
    st.sidebar.markdown(f"Bienvenido, {st.session_state['username']}")
    st.sidebar.button("Cerrar Sesión", on_click=logout)

    data_path = 'data/ventas_corto_eliminar.xlsx'
    data = pd.read_excel(data_path)

    # Configurar la barra lateral
    st.sidebar.title("Opciones de Visualización")
    page = st.sidebar.selectbox("Selecciona la Página", ["Tabla de Ventas", "Análisis Gráfico"])

    # Página: Tabla de Ventas
    if page == "Tabla de Ventas":
        st.title("Dashboard de Ventas")
        st.header("Datos de Ventas")
        st.dataframe(data)

        # Gráfica de ventas por país
        st.header("Ventas Totales por País")
        ventas_por_pais = data.groupby('Pais')['Total'].sum()
        st.bar_chart(ventas_por_pais)

        # Métricas
        st.header("Métricas")
        total_ventas = data['Total'].sum()
        total_cantidad = data['Cantidad'].sum()
        st.metric(label="Total de Ventas", value=f"${total_ventas:,.2f}")
        st.metric(label="Total de Cantidad Vendida", value=total_cantidad)

    # Página: Análisis Gráfico
    if page == "Análisis Gráfico":
        st.title("Análisis Gráfico de Ventas")

        # Gráfico de dispersión
        st.header("Gráfico de Dispersión")
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x='Cantidad', y='Total', hue='Pais', ax=ax)
        st.pyplot(fig)

        # Gráfico de barras
        st.header("Gráfico de Barras")
        fig, ax = plt.subplots()
        ventas_por_cliente = data.groupby('IdCliente')['Total'].sum().nlargest(5)
        ventas_por_cliente.plot(kind='bar', ax=ax, color=['blue', 'orange'])
        st.pyplot(fig)

        # Preparar datos para el gráfico de línea
        ventas_por_cliente = data.groupby('IdCliente')['Total'].sum().nlargest(5)
        line_data = pd.DataFrame(ventas_por_cliente).reset_index()
        line_data.columns = ['Cliente', 'Ventas Totales']

        # Gráfico de línea v2
        st.header("Ventas Totales por Cliente")
        st.line_chart(line_data.set_index('Cliente'))

        # Gráfico de dona
        # st.header("Gráfico de Dona")
        # fig, ax = plt.subplots()
        # ventas_por_pais = data.groupby('Pais')['Total'].sum()
        # ventas_por_pais.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
        # ax.axis('equal')  # Para hacer un gráfico circular
        # st.pyplot(fig)

        ventas_por_pais = data.groupby('Pais')['Total'].sum().reset_index()

        st.header("Gráfico de Dona")
        pie_chart = px.pie(ventas_por_pais,
                        title='Ventas por País',
                        values='Total',
                        names='Pais',
                        hole=0.4)  # Centro hueco para el efecto de dona

        st.plotly_chart(pie_chart)

        # Gráfico de área
        st.header("Ventas por País")
        st.area_chart(ventas_por_pais.set_index('Pais'))
