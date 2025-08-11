import streamlit as st
from config import ConfiguracionDePagina, CrearEncabezado
import json

# === Configuración de página ===
ConfiguracionDePagina()

# === Usuarios fijos ===
USERS = {"Benjita": "0308", "Inge" : "21300573"}

# === Pestañas ===
pestañas = ["Principal"]

@st.cache_data
def cargar_index_to_label():
    with open("index_to_label.json", "r") as f:
        return json.load(f)

index_to_label = cargar_index_to_label()

@st.cache_resource
def cargar_modelo():
    import tensorflow as tf
    modelo = tf.keras.models.load_model("dinoNet.h5")
    return modelo
dinoNet = cargar_modelo()

def predecir_dinosaurio(pil_image, index_to_label):
    import tensorflow as tf
    import numpy as np
    
    image = np.array(pil_image)
    if image.shape[-1] == 4:
        image = image[..., :3]
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    image = tf.image.resize(image, (224, 224))
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)  
    pred = dinoNet.predict(image)
    pred_idx = np.argmax(pred, axis=1)[0]

    dino = index_to_label[str(pred_idx)]
    return dino

# === Inicia sesión ===
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# === si no esta logueado ===
if not st.session_state["logged_in"]:
    CrearEncabezado()
    st.title("Inicio de sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if username in USERS and password == USERS[username]:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"¡Bienvenido, {username}!")
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")

# ===  Si esta logueado ===
else:
    PK = True
    st.sidebar.write(f"👤 Usuario: {st.session_state['username']}")
    if st.sidebar.button("Cerrar sesión 🔒"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

    opcion = st.sidebar.radio(
        "Selecciona una pestaña:",
        pestañas
    )

    if opcion == "Principal":
        st.title("Predicción de Dinosaurio")
        st.text("Esta es una dino App para dino Apasionados que quieran apoyar")

        st.markdown("### Dinosaurios que se pueden predecir:")
        nombres_dinos = list(index_to_label.values())
        for dino in nombres_dinos:
            st.write(f"- {dino}")


        archivo = st.file_uploader("Sube una imagen de un dinosaurio", type=["png", "jpg", "jpeg"])

        if archivo is not None:
            from PIL import Image
            import os
            from datetime import datetime
            imagen = Image.open(archivo)
            st.image(imagen, caption="Imagen subida")
            if st.button("Predecir dinosaurio"):
                # ---------------- Guardamos las imagenes ----------------------
                carpeta_guardado = "public_data_images"
                if not os.path.exists(carpeta_guardado):
                    os.makedirs(carpeta_guardado)
                nombre_base, extension = os.path.splitext(archivo.name)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_unico = f"{nombre_base}_{timestamp}{extension}"
                ruta_guardado = os.path.join(carpeta_guardado, nombre_unico)
                with open(ruta_guardado, "wb") as f:
                    f.write(archivo.getbuffer())
            # ---------------- Guardamos las imagenes ----------------------
                resultado = predecir_dinosaurio(imagen, index_to_label)
                st.success(f"El dinosaurio detectado es: {resultado}")

