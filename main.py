# Proyecto: Sistema de Gestión Académica
# Tecnología: Streamlit + MySQL + Docker o Cloud

import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

# -------- CONFIGURACIÓN DE CONEXIÓN -------- #
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["db_host"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        database=st.secrets["db_name"]
    )

# -------- EXPORTAR GRÁFICO COMO IMAGEN -------- #
def exportar_grafico(figura, nombre_archivo):
    buffer = BytesIO()
    figura.write_image(buffer, format="png")
    st.download_button(
        label=f"⬇️ Descargar {nombre_archivo} como imagen",
        data=buffer.getvalue(),
        file_name=f"{nombre_archivo}.png"
    )

# -------- PLACEHOLDERS DE MÓDULOS -------- #
def gestion_dashboard():
    st.subheader("📊 Dashboard")
    st.success("Módulo dashboard implementado previamente con resumen de estudiantes, pagos, clases, y gráficos interactivos.")


def gestion_estudiantes():
    st.subheader("🧑‍🎓 Gestión de Estudiantes")
    st.success("Este módulo permite registrar, editar y listar estudiantes, tutores, información de contacto y cursos.")


def gestion_profesores():
    st.subheader("👨‍🏫 Gestión de Profesores")
    st.success("Este módulo permite gestionar profesores, sus cursos asignados, contactos y disponibilidad.")


def gestion_cursos():
    st.subheader("📚 Gestión de Cursos")
    st.success("Aquí puedes registrar, editar y listar todos los cursos activos en la academia.")


def gestion_clases():
    st.subheader("📅 Gestión de Clases y Calendario")
    st.success("Este módulo muestra clases programadas por fecha, profesores, y permite vista tipo calendario.")


def gestion_pagos():
    st.subheader("💰 Gestión de Pagos")
    st.success("Módulo para registrar, filtrar y exportar pagos, incluyendo alertas de vencimiento.")


def gestion_calificaciones():
    st.subheader("📈 Gestión de Calificaciones y Asistencia")
    st.success("Incluye ingreso de notas, estadísticas, y asistencia por curso con exportación de gráficos.")

# -------- INICIO -------- #
def main():
    st.set_page_config(layout="wide")
    st.title("🎓 Sistema de Gestión Académica")
    st.sidebar.title("Menú Principal")

    menu = [
        "Dashboard", 
        "Estudiantes", 
        "Profesores", 
        "Cursos", 
        "Clases y Calendario", 
        "Pagos", 
        "Calificaciones y Asistencia"
    ]

    opcion = st.sidebar.selectbox("Selecciona un módulo", menu)

    if opcion == "Dashboard":
        gestion_dashboard()
    elif opcion == "Estudiantes":
        gestion_estudiantes()
    elif opcion == "Profesores":
        gestion_profesores()
    elif opcion == "Cursos":
        gestion_cursos()
    elif opcion == "Clases y Calendario":
        gestion_clases()
    elif opcion == "Pagos":
        gestion_pagos()
    elif opcion == "Calificaciones y Asistencia":
        gestion_calificaciones()

if __name__ == '__main__':
    main()
