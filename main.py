
# Proyecto: Sistema de Gestión Académica
# Tecnología: Streamlit + MySQL + Docker o Cloud

import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
from fpdf import FPDF
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

# -------- SESIÓN -------- #
if 'role' not in st.session_state:
    st.session_state.role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# -------- EXPORTAR GRÁFICO COMO IMAGEN -------- #
def exportar_grafico(figura, nombre_archivo):
    buffer = BytesIO()
    figura.write_image(buffer, format="png")
    st.download_button(
        label=f"⬇️ Descargar {nombre_archivo} como imagen",
        data=buffer.getvalue(),
        file_name=f"{nombre_archivo}.png"
    )

# -------- GESTIÓN DE CALIFICACIONES -------- #
def gestion_calificaciones():
    st.subheader("📚 Gestión de Calificaciones")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre FROM cursos")
    cursos = cursor.fetchall()
    curso_dict = {c['nombre']: c['id'] for c in cursos}
    curso_nombre = st.selectbox("Seleccionar Curso", list(curso_dict.keys()))

    if curso_nombre:
        curso_id = curso_dict[curso_nombre]

        cursor.execute("""
            SELECT e.id, e.nombre
            FROM estudiantes e
            JOIN estudiante_curso ec ON ec.estudiante_id = e.id
            WHERE ec.curso_id = %s
        """, (curso_id,))
        estudiantes = cursor.fetchall()

        for est in estudiantes:
            calificacion = st.number_input(f"{est['nombre']}", key=est['id'], min_value=0.0, max_value=100.0, step=0.1)
            if st.button(f"Guardar {est['nombre']}", key=f"btn_{est['id']}"):
                cursor.execute("""
                    INSERT INTO calificaciones (estudiante_id, curso_id, nota, fecha)
                    VALUES (%s, %s, %s, %s)
                """, (est['id'], curso_id, calificacion, datetime.today()))
                conn.commit()
                st.success(f"Nota guardada para {est['nombre']}")

    st.subheader("📄 Historial de Calificaciones")
    cursor.execute("""
        SELECT e.nombre AS estudiante, c.nombre AS curso, ca.nota, ca.fecha
        FROM calificaciones ca
        JOIN estudiantes e ON ca.estudiante_id = e.id
        JOIN cursos c ON ca.curso_id = c.id
        ORDER BY ca.fecha DESC
    """)
    historial = cursor.fetchall()

    if historial:
        df = pd.DataFrame(historial)
        st.dataframe(df)

        promedio_general = df['nota'].mean()
        st.success(f"📊 Promedio General del Curso: {promedio_general:.2f}")

        fig, ax = plt.subplots(figsize=(8,4))
        df_sorted = df.sort_values("fecha")
        df_grouped = df_sorted.groupby("fecha")["nota"].mean().reset_index()
        ax.plot(df_grouped['fecha'], df_grouped['nota'], marker='o')
        ax.set_title("Promedio General por Fecha")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Promedio Nota")
        ax.grid(True)
        st.pyplot(fig)

        fig_dist = px.histogram(df, x="nota", nbins=10, title="Distribución de Notas")
        st.plotly_chart(fig_dist, use_container_width=True)
        exportar_grafico(fig_dist, "distribucion_notas")

        df_cantidades = df.groupby("curso")["nota"].count().reset_index(name="Cantidad de Notas")
        fig_curso = px.bar(df_cantidades, x="curso", y="Cantidad de Notas", title="Cantidad de Notas por Curso")
        st.plotly_chart(fig_curso, use_container_width=True)
        exportar_grafico(fig_curso, "cantidad_notas_por_curso")

        # -------- GRAFICO DE ASISTENCIA -------- #
        cursor.execute("""
            SELECT e.nombre AS estudiante, c.nombre AS curso, a.estado, a.fecha
            FROM asistencia a
            JOIN estudiantes e ON a.estudiante_id = e.id
            JOIN cursos c ON a.curso_id = c.id
            ORDER BY a.fecha DESC
        """)
        asistencia = cursor.fetchall()
        if asistencia:
            df_asis = pd.DataFrame(asistencia)
            st.subheader("📈 Historial de Asistencia")
            st.dataframe(df_asis)
            df_asis_count = df_asis.groupby(["curso", "estado"]).size().reset_index(name="Cantidad")
            fig_asis = px.bar(df_asis_count, x="curso", y="Cantidad", color="estado", barmode="group", title="Resumen de Asistencia por Curso")
            st.plotly_chart(fig_asis, use_container_width=True)
            exportar_grafico(fig_asis, "asistencia_por_curso")
            st.download_button("⬇️ Descargar asistencia en Excel", data=df_asis.to_excel(index=False), file_name="asistencia.xlsx")
        else:
            st.info("No hay datos de asistencia registrados.")

        st.download_button("⬇️ Descargar calificaciones en Excel", data=df.to_excel(index=False), file_name="calificaciones.xlsx")
    else:
        st.info("No hay calificaciones registradas aún.")

# -------- INICIO -------- #
def main():
    st.title("📚 Sistema de Gestión Académica")
    st.sidebar.title("Menú")
    opcion = st.sidebar.selectbox("Selecciona una opción", ["Calificaciones"])

    if opcion == "Calificaciones":
        gestion_calificaciones()

if __name__ == "__main__":
    main()
