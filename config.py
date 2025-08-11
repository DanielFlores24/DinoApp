import streamlit as st

def CrearEncabezado():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("DinoLogo.png", width=380) 
    with col2:
        st.markdown("""
            <h1 style='font-size:60px; color:#A7727D;'>Dino App</h1>
            <h2 style='font-size:28px; color:#E0E0E0;'>Aplicación para dinosaurios</h2>
        """, unsafe_allow_html=True)
        
def ConfiguracionDePagina():
    #Configuracion de la pagina
    st.set_page_config(
        page_title="Dino App",
        page_icon="🦖",
        initial_sidebar_state="expanded",
    )
    #Configuraciones extra
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    #Barra Lateral
    st.sidebar.image("DinoLogo.png", width=400)
    st.sidebar.markdown(
        """
        <h1 style='font-size: 60px;color:#A7727D;'>Dino App</h1>
        <h3 style='font-size: 24px;color:#FFFFFF;'>Aplicación para dinosaurios</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] .stRadio > label div {font-size: 24px;  }
        </style>
        """,
        unsafe_allow_html=True,
    )

