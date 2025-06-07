import streamlit as st
import pandas as pd
from utils.utils import *

# Mostra i corsi disponibili
def show_corsi_section():
    try:
        # Query per ottenere tutti i corsi e i tipi distinti pe rle metriche 
        query_all_corsi = "SELECT * FROM Corsi"
        corsi = execute_query(st.session_state["connection"], query_all_corsi)
        df_corsi = pd.DataFrame(corsi)
        
        # Query tipi distinti deii corsi
        query_tipi = "SELECT DISTINCT Tipo FROM Corsi"
        tipi = execute_query(st.session_state["connection"], query_tipi)
        df_tipi = pd.DataFrame(tipi)
        
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Numero di Corsi", len(df_corsi))
        with col2:
            st.metric("Numero di Tipi di Corsi", len(df_tipi))
        
        st.markdown("---")
        with st.expander("## Filtra i corsi", expanded=False):
            st.markdown("Utilizza i filtri per trovare i corsi che ti interessano.")
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
    
        # Filtro per il tipo di corso
        if tipi_selezionati:
            tipi_str = "', '".join(tipi_selezionati)
            query_filtro += f" AND C.Tipo IN ('{tipi_str}')"
        
        
        corsi_filtrati = execute_query(st.session_state["connection"], query_filtro)
        df_risultati = pd.DataFrame(corsi_filtrati)
        
        st.markdown("### 📋 Corsi Disponibili")
        
        if df_risultati.empty:
            st.warning("Nessun corso trovato con i criteri selezionati.")
            return
        
        df_visualizza = df_risultati.rename(columns={
            'CodC': 'Codice', 
            'Nome': 'Nome Corso', 
            'Tipo': 'Categoria',
            'Livello': 'Difficoltà'
        })
                
        st.dataframe(df_visualizza, use_container_width=True)
        st.caption(f"Trovati {len(df_visualizza)} corsi che corrispondono ai criteri selezionati")
        
        
        # st.dataframe(df_risultati, use_container_width=True)
        
        # esxpander per programmi e istruttori
        with st.expander("Programmi e Istruttori", expanded=False):
            show_programmi_section(df_risultati)
                
    except Exception as e:
        st.error(f"Errore durante il caricamento dei corsi: {e}")
        return False

def show_programmi_section(df_risultati):
    try:
        cod_corsi = df_risultati['CodC'].tolist()
        
        if not cod_corsi:
            st.warning("Nessun corso selezionato")
            return
        
        cod_str = ", ".join([f"'{str(cod)}'" for cod in cod_corsi])
        
        query_programmi = f"""
        SELECT C.Nome AS Corso, P.Giorno, P.OraInizio AS 'Ora Inizio', P.Durata AS 'Durata (min)',CONCAT(I.Nome, ' ', I.Cognome) AS Istruttore, I.Email 
        FROM Programma P, Corsi C, Istruttore I
        WHERE P.CodC IN ({cod_str}) AND P.CodC = C.CodC AND P.CodFisc = I.CodFisc
        ORDER BY C.Nome, P.Giorno, P.OraInizio
        """
        
        programmi = execute_query(st.session_state["connection"], query_programmi)
        df_programmi = pd.DataFrame(programmi)
        
        if df_programmi.empty:
            st.warning("Nessun programma trovato per i corsi selezionati.")
        else:
            st.dataframe(df_programmi, use_container_width=True)
            
    except Exception as e:
        st.error(f"Errore durante il caricamento dei programmi: {e}")
        return False


if __name__ == "__main__":
    st.set_page_config(
        page_title="Corsi Disponibili",
        layout="wide",
        page_icon="🤸🏻‍♂️",
        initial_sidebar_state="expanded"
    )
    st.title("🤸🏻‍♂️ Corsi Disponibili")
    st.markdown("Visualizza e filtra i corsi disponibili nella palestra")
    
    # Verifica della connessione al database e mostra i dati
    if check_connection():
        show_corsi_section()
