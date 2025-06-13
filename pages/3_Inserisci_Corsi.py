import streamlit as st
from utils.utils import *
from sqlalchemy import text


def validate_input_course(cod_c, nome, tipo, livello):
    """Valida i dati del corso prima dell'inserimento"""
    errors = []
    
    # No Campi vuoti
    if not cod_c:
        errors.append("Il Codice Corso è obbligatorio")
    if not nome:
        errors.append("Il Nome è obbligatorio")
    if not tipo:
        errors.append("Il Tipo è obbligatorio")
    
    if cod_c and not cod_c.startswith("CT"):
        errors.append("Il Codice Corso deve iniziare con 'CT'")
    if livello < 1 or livello > 4:
        errors.append("Il Livello deve essere compreso tra 1 e 4")
    if not isinstance(livello, int):
        errors.append("Il Livello deve essere un numero intero")
    if len(cod_c) > 10:
        errors.append("Il Codice Corso non può superare i 10 caratteri")
    if len(nome) > 50:
        errors.append("Il Nome Corso non può superare i 50 caratteri")
    if len(tipo) > 50:
        errors.append("Il Tipo Corso non può superare i 50 caratteri")
    
    return errors

def insert_new_course():
    with st.form("corso_form"):
        col1, col2 = st.columns(2)
        
        # Campo CodC
        cod_c = col1.text_input("Codice Corso", placeholder="Es. CT123",help="Il codice deve iniziare con 'CT'")
        
        # Nome
        nome = col2.text_input("Nome Corso", placeholder="Es. Yoga Principianti", help="Inserisci il nome completo del corso")
        
        # Tipo 
        tipo = col1.text_input("Tipo Corso:",placeholder="Es. Fitness, Yoga, Nuoto",help="Inserisci il tipo di corso")
        
        # Livello
        livello = col2.number_input("Livello", 
                                   min_value=1, 
                                   max_value=4,
                                   value=1,
                                   help="Livello di difficoltà (da 1 a 4)")
        
        # Bottone
        submit_button = st.form_submit_button("Inserisci Corso", type="primary")
    
    
    if submit_button:
        
        errors = validate_input_course(cod_c, nome, tipo, livello)
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Validazione Ok
            try:
                
                insert_query = f"""
                INSERT INTO Corsi (CodC, Nome, Tipo, Livello) 
                VALUES ('{cod_c}', '{nome}', '{tipo}', {livello})
                """
                
                execute_query(st.session_state["connection"],insert_query)
                st.session_state["connection"].commit()
                
                st.success(f"Corso '{nome}' inserito con successo!")
                
                # Dettagli
                st.info(f"""
                    **Dettagli Corso Inserito:**
                    - **Codice:** {cod_c}
                    - **Nome:** {nome}
                    - **Tipo:** {tipo}
                    - **Livello:** {livello}
                    """
                )
                
            except Exception as e:
                error_msg = str(e)
                if "Duplicate entry" in error_msg:
                    st.error(f"Errore: Codice corso '{cod_c}' già esistente.")
                else:
                    st.error(f"Errore durante l'inserimento del corso: {error_msg}")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Inserimento Corsi",
        page_icon="➕",
        initial_sidebar_state="expanded"
    )
    
    st.title("➕ Inserimento Nuovo Corso")
    st.markdown("Inserisci i dati del nuovo corso da aggiungere")
    
    # Verifica della connessione al database e mostra il form
    if check_connection():
        insert_new_course()