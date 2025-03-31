# 🎓 Sistema de Gestión Académica (Streamlit + MySQL)

Este es un sistema completo para academias que permite gestionar estudiantes, profesores, cursos, clases, calificaciones, asistencias y pagos. Desarrollado con **Streamlit** y conectado a **MySQL en la nube**.

---

## 🚀 Cómo desplegar en Streamlit Cloud

### 1. Requisitos

- Tener una cuenta en [Streamlit Cloud](https://streamlit.io/cloud)
- Tener una base de datos MySQL accesible (recomendado: [PlanetScale](https://planetscale.com), [Railway](https://railway.app), etc.)

---

### 2. Estructura esperada

```
📁 mi-repo/
├── main.py
├── requirements.txt
├── init_academia.sql  # Script para crear tablas
└── modules/
    ├── auth.py
    ├── dashboard.py
    ├── estudiantes.py
    ├── profesores.py
    ├── cursos.py
    ├── clases.py
    ├── pagos.py
    ├── calificaciones.py
    └── asistencia.py
```

---

### 3. Configurar la base de datos

1. Crea la base de datos en tu proveedor
2. Ejecuta el archivo `init_academia.sql` para crear las tablas y cargar datos de ejemplo

---

### 4. Configurar Secrets

En la app de Streamlit Cloud ve a `Settings > Secrets` y coloca lo siguiente:

```toml
db_host = "TU_SERVIDOR_MYSQL"
db_user = "TU_USUARIO"
db_password = "TU_CONTRASEÑA"
db_name = "academia"
```

---

### 5. Crear la app

1. Entra a [streamlit.io/cloud](https://streamlit.io/cloud)
2. Crea una nueva app conectando tu GitHub
3. Selecciona el repositorio y el archivo `main.py`
4. ¡Listo! 🎉

---

## 👤 Usuarios de ejemplo

- Admin → `admin@academia.com` / `admin123`
- Profesor → `profe@academia.com` / `profe123`
- Estudiante → `alumno@academia.com` / `alumno123`

---

## 🛠 Stack utilizado

- Streamlit
- MySQL
- Plotly
- Pandas
- SHA-256 para autenticación
