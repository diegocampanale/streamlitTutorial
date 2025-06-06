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
        
        # Filtra corsi
        st.markdown("### Filtra Corsi")
        
        filter_col1, filter_col2 = st.columns(2)
        
        tipi_corsi = df_tipi['Tipo'].tolist()
        tipi_selezionati = filter_col1.multiselect("Seleziona Tipo di Corso:", options=tipi_corsi, default=[])
        
        # FIltro per livello di difficoltà
        min_level, max_level = int(df_corsi['Livello'].min()), int(df_corsi['Livello'].max())
        livello_range = filter_col2.slider(
            "Seleziona Range di Difficoltà:",
            min_value=min_level,
            max_value=max_level,
            value=(min_level, max_level)
        )
        
        # query di filtraggio
        query_filtro = f"""
        SELECT C.CodC, C.Nome, C.Tipo, C.Livello
        FROM Corsi C
        WHERE C.Livello BETWEEN {livello_range[0]} AND {livello_range[1]}
        """
        
        # Filtro tipo 
        if tipi_selezionati:
            tipi_str = "', '".join(tipi_selezionati)
            query_filtro += f" AND C.Tipo IN ('{tipi_str}')"
            
        # Esecuzione query filtro
        corsi_filtrati = execute_query(st.session_state["connection"], query_filtro)
        df_risultati = pd.DataFrame(corsi_filtrati)
        
        st.markdown("### Risultati Filtrati")
        
        if df_risultati.empty:
            st.warning("Nessun corso trovato con i criteri selezionati.")
            return
        st.dataframe(df_risultati, use_container_width=True)
                
    except Exception as e:
        st.error(f"Errore durante il caricamento dei corsi: {e}")
        return False


if __name__ == "__main__":
    st.title("🤸🏻‍♂️ Corsi Disponibili")
    
    # Verifica della connessione al database e mostra i dati
    if check_connection():
        show_corsi_section()
