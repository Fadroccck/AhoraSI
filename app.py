import streamlit as st
import pandas as pd
import os
from jinja2 import Template
from templates.home import home_view
from templates.grafico1 import grafico1_view
from templates.grafico2 import grafico2_view
from templates.tablero import tablero_view

def cargar_plantilla(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        plantilla = archivo.read()
    return plantilla

def mostrar_encabezado():
    header_html = cargar_plantilla('header.html')
    template = Template(header_html)
    contenido = template.render(usuario=st.session_state['usuario'])
    st.markdown(contenido, unsafe_allow_html=True)

def mostrar_sidebar():
    sidebar_html = cargar_plantilla('sidebar.html')
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
    pagina = st.sidebar.radio("Navegación", ["Home", "Gráfico 1", "Gráfico 2", "Tablero"])
    
    datasets = os.listdir('data')
    dataset_seleccionado = st.sidebar.selectbox("Seleccione un dataset", datasets)
    st.session_state['dataset'] = dataset_seleccionado

    fecha = st.sidebar.date_input("Seleccione una fecha")
    st.session_state['fecha_filtro'] = fecha

    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state['usuario']
        del st.session_state['pagina']
        del st.session_state['dataset']
        del st.session_state['fecha_filtro']
        st.experimental_rerun()

    return pagina

def iniciar_sesion():
    st.title("Inicio de Sesión")

    nombre = st.text_input("Nombre de usuario")
    contrasena = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if nombre == "administrador" and contrasena == "password":
            st.session_state['usuario'] = nombre
            st.session_state['pagina'] = "Home"
            st.session_state['dataset'] = os.listdir('data')[0]
            st.session_state['fecha_filtro'] = pd.to_datetime('today')
            st.success("Sesión iniciada con éxito")
            st.experimental_rerun()  
        else:
            st.error("Nombre de usuario o contraseña incorrectos")

def mostrar_dashboard():
    mostrar_encabezado()
    pagina = mostrar_sidebar()

    if pagina == "Home":
        home_view(st.session_state['usuario'], st.session_state['dataset'], st.session_state['fecha_filtro'])
    elif pagina == "Gráfico 1":
        grafico1_view(st.session_state['dataset'], st.session_state['fecha_filtro'])
    elif pagina == "Gráfico 2":
        grafico2_view(st.session_state['dataset'], st.session_state['fecha_filtro'])
    elif pagina == "Tablero":
        tablero_view(st.session_state['dataset'], st.session_state['fecha_filtro'])

def main():
    if 'usuario' not in st.session_state:
        iniciar_sesion()
    else:
        mostrar_dashboard()

if __name__ == "__main__":
    main()
