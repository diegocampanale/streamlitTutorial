import streamlit as st
import pandas as pd
from utils.utils import *

# Mostra i corsi disponibili
def show_corsi_section():
    try:
        # Query tutti i corsi
        query_all_corsi = "SELECT * FROM Corsi"
        corsi = execute_query(st.session_state["connection"], query_all_corsi)
        df_corsi = pd.DataFrame(corsi)
        
        # Query tipi distinti di corsi
        query_tipi = "SELECT DISTINCT Tipo FROM Corsi"
        tipi = execute_query(st.session_state["connection"], query_tipi)
        df_tipi = pd.DataFrame(tipi)
        
        # Mostra le metriche in colonne
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Numero di Corsi", len(df_corsi))
        with col2:
            st.metric("Numero di Tipi di Corsi", len(df_tipi))
        
        st.markdown("---")
        
    except Exception as e:
        st.error(f"Errore durante il caricamento dei corsi: {e}")
        return False


# Configurazioni pagina
st.set_page_config(
    page_title="Corsi Disponibili",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dbdmg.polito.it/',
        'Report a bug': "https://dbdmg.polito.it/",
        'About': "# Corso di *Basi di Dati*"
    }
)
