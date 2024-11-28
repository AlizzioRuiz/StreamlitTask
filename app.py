import streamlit as st
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  
    return conn


def setup_database():
    try:
        conn = get_db_connection()  # DB connect
        cursor = conn.cursor()  # The cursor is created
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)  # The table is created
        conn.commit()  # Save the changes
    except sqlite3.Error as e:  # If any error occurs
        st.error(f"Error al configurar la base de datos: {e}")
    finally:
        conn.close()  


# Add user
def add_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Get users
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


setup_database()

# Streamlit interface
st.title("Login Streamlit WELCOME")

# sign the user
st.header("Registrar Usuario")
username = st.text_input("Nombre de usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Registrar"):
    if username and password:
        add_user(username, password)
        st.success("Usuario registrado con éxito")
    else:
        st.error("Por favor, completa todos los campos")

# show the users
st.header("Usuarios Registrados")
users = get_users()

for user in users:
    st.text(f"ID: {user[0]}, Usuario: {user[1]}")
