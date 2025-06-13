import streamlit as st
from utils.utils import *

def get_istruttori():
    query = """
    SELECT CodFisc, CONCAT(Nome, ' ', Cognome) as NomeCompleto
    FROM Istruttore
    ORDER BY Cognome, Nome
    """
    result = execute_query(st.session_state["connection"], query)
    codici = []
    nomi = []
    for row in result:
        codici.append(row[0])
        nomi.append(row[1])
    return codici, nomi

def get_corsi():
    query = """
    SELECT CodC, Nome as NomeCorso
    FROM Corsi
    ORDER BY CodC
    """
    result = execute_query(st.session_state["connection"], query)
    codici = []
    nomi = []
    for row in result:
        codici.append(row[0])
        nomi.append(row[1])
    return codici, nomi

def validate_input_lezione(cod_fisc, giorno, ora_inizio, durata, cod_c, sala):
    errors = []
    
    # Verifica campi obbligatori
    if not cod_fisc:
        errors.append("Il Codice Fiscale dell'istruttore è obbligatorio")
    if not giorno:
        errors.append("Il Giorno è obbligatorio")
    if not cod_c:
        errors.append("Il Codice Corso è obbligatorio")
    if not sala:
        errors.append("La Sala è obbligatoria")
    
    # Validazione della durata (max 60 minuti)
    if durata > 60:
        errors.append("La durata della lezione non può superare 60 minuti")
    
    # Validazione del giorno (solo Lunedì-Venerdì)
    giorni_validi = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    if giorno not in giorni_validi:
        errors.append("Il giorno deve essere compreso tra Lunedì e Venerdì")
    
    return errors

def check_lezione_esistente(cod_c, giorno): 
    query = f"""
    SELECT COUNT(*) as count
    FROM Programma
    WHERE CodC = '{cod_c}' AND Giorno = '{giorno}'
    """
    result = execute_query(st.session_state["connection"], query).fetchone()
    return result[0] > 0

def insert_new_lezione():
    with st.form("lezione_form"):
        col1, col2 = st.columns(2)
        
        try:
            # Recupero delle liste di istruttori e corsi
            codici_istruttori, nomi_istruttori = get_istruttori()
            codici_corsi, info_corsi = get_corsi()

            istruttori_map = {cf: nome for cf, nome in zip(codici_istruttori, nomi_istruttori)}
            corsi_map = {cf: info for cf, info in zip(codici_corsi, info_corsi)}
            
            # input Istruttore
            cod_fisc = col1.selectbox(
                "Istruttore", 
                options=codici_istruttori,
                format_func=lambda x: f"{x} - {istruttori_map.get(x, '')}",
                help="Seleziona l'istruttore che terrà la lezione"
            )
            
            # Input giorno
            giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
            giorno = col2.selectbox(
                "Giorno della Settimana",
                options=giorni,
                help="Seleziona il giorno in cui si terrà la lezione"
            )
            
            # input orario
            ora_inizio = col1.slider(
                "Ora di Inizio",
                min_value=8,
                max_value=20,
                value=14,
                step=1,
                help="Seleziona l'ora di inizio della lezione"
            )
            
            # Input durata
            durata = col2.slider(
                "Durata (minuti)",
                min_value=15,
                max_value=60,
                value=45,
                step=15,
                help="Seleziona la durata della lezione (max 60 minuti)"
            )
            
            # Input corso
            cod_c = col1.selectbox(
                "Corso",
                options=codici_corsi,
                format_func=lambda x: f"{x} - {corsi_map.get(x, x)}",
                help="Seleziona il corso per cui programmare la lezione"
            )
            
            # Input sala
            sala = col2.text_input(
                "Sala",
                placeholder="Es. S1, S2",
                help="Inserisci il nomeo della sala dove si terrà la lezione"
            )
            
            # Bottone
            submit_button = st.form_submit_button("Inserisci Lezione", type="primary")
            
        except Exception as e:
            st.error(f"Errore durante il recupero dei dati: {e}")
            return
    
    if submit_button:
        # Validazione dati
        errors = validate_input_lezione(cod_fisc, giorno, ora_inizio, durata, cod_c, sala)
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Controllo se esiste già una lezione per lo stesso corso nello stesso giorno
            if check_lezione_esistente(cod_c, giorno):
                st.error(f"Errore: Esiste già una lezione programmata per il corso {cod_c} nel giorno {giorno}.")
            else:
                # Validazione OK
                try:
                    # Formatta correttamente l'orario con gestione delle mezze ore
                    ora_intero = int(ora_inizio)
                    minuti = 30 if ora_inizio % 1 > 0 else 0
                    ora_formattata = f"{ora_intero:02d}:{minuti:02d}:00"
                    
                    # Query
                    insert_query = f"""
                    INSERT INTO Programma (CodFisc, Giorno, OraInizio, Durata, CodC, Sala) 
                    VALUES ('{cod_fisc}', '{giorno}', '{ora_formattata}', {durata}, '{cod_c}', '{sala}')
                    """
                    
                    execute_query(st.session_state["connection"], insert_query)
                    st.session_state["connection"].commit()
                    
                    st.success(f"Lezione inserita con successo!")
                    
                    # Mostra dettagli della lezione
                    st.info(f"""
                    **Dettagli Lezione Inserita:**
                    - **Istruttore:** {cod_fisc} - {istruttori_map.get(cod_fisc, "")}
                    - **Corso:** {cod_c} - {corsi_map.get(cod_c, "")}
                    - **Giorno:** {giorno}
                    - **Ora Inizio:** {ora_formattata}
                    - **Durata:** {durata} minuti
                    - **Sala:** {sala}
                    """)
                    
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"Errore durante l'inserimento della lezione: {error_msg}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Inserimento Lezioni",
        page_icon="📅",
        initial_sidebar_state="expanded"
    )
    
    st.title("📅 Inserimento Nuova Lezione")
    st.markdown("Inserisci i dati per programmare una nuova lezione settimanale")
    
    # Verifica della connessione al database e mostra il form
    if check_connection():
        insert_new_lezione()
