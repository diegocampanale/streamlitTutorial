import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *

st.set_page_config(
    page_title="Homepage",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dbdmg.polito.it/',
        'Report a bug': "https://dbdmg.polito.it/",
        'About': "# Corso di *Basi di Dati*"
    }
)


st.title("Quaderno 4")
st.markdown("Sviluppo di un’applicazione web con Streamlit e MySQL")
st.markdown("### Obiettivi")
st.markdown("Creare un’applicazione web in Python (Streamlit) in grado di interagire con un database MySQL in modo da eseguire interrogazioni in base alle interazioni dell’utente.")
st.markdown("### Studente")
st.markdown("Realizzato da **Diego Campanale** (Matricola: s325040)")


st.markdown("---")
st.markdown("## Lezioni Programmate")

# Verifica la connessione al database
if st.session_state.get("connection"):
    conn = st.session_state["connection"]
    
    # Query per lezioni per slot di tempo
    query_time_slots = """
    SELECT OraInizio AS Ora, COUNT(*) AS NumeroLezioni
    FROM Programma
    GROUP BY OraInizio
    ORDER BY OraInizio
    """
    
    # Query per lezioni per giorno della settimana
    query_week_days = """
    SELECT Giorno, COUNT(*) AS NumeroLezioni
    FROM Programma
    GROUP BY Giorno
    """
    
    try:
        # Esegui le query e ottieni i dati
        data_time_slots = pd.read_sql(query_time_slots, conn)
        data_week_days = pd.read_sql(query_week_days, conn)
        
        # Area Chart
        st.markdown("#### Lezioni per Slot di Tempo")
        st.area_chart(data_time_slots.set_index("Ora"))
        
        
        mapping_giorni = {
            'Lunedì': '1 - Lunedì',
            'Martedì': '2 - Martedì',
            'Mercoledì': '3 - Mercoledì',
            'Giovedì': '4 - Giovedì',
            'Venerdì': '5 - Venerdì',
            'Sabato': '6 - Sabato',
            'Domenica': '7 - Domenica'
        }
        
        # Applica la mappatura
        data_week_days['GiornoOrdinato'] = data_week_days['Giorno'].map(mapping_giorni)
        
        st.markdown("#### Lezioni per Giorno della Settimana")
        st.bar_chart(data_week_days.set_index("GiornoOrdinato")['NumeroLezioni'])
        
    except Exception as e:
        st.error(f"Errore durante il recupero dei dati: {e}")
else:
    st.warning("Connettiti al database per visualizzare i dati delle lezioni.")

if "connection" not in st.session_state.keys():
        st.session_state["connection"]=False
        
check_connection()