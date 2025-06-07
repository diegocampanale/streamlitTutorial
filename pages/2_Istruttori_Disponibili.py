import streamlit as st
import pandas as pd
import random
import datetime
from utils.utils import *

def show_istruttori_section():
    try:
        
        query_all_istruttori = """
        SELECT CodFisc, Nome, Cognome, DataNascita, Email, Telefono
        FROM Istruttore
        ORDER BY Cognome, Nome
        """
        
        istruttori = execute_query(st.session_state["connection"], query_all_istruttori)
        df_istruttori = pd.DataFrame(istruttori)
        
        if df_istruttori.empty:
            st.warning("Nessun istruttore presente nel database della palestra.")
            return False

        if 'DataNascita' in df_istruttori.columns:
            min_date = df_istruttori['DataNascita'].min()
            max_date = df_istruttori['DataNascita'].max()
        else:
            min_date = datetime.date(1950, 1, 1)
            max_date = datetime.date.today()
            
        with st.expander("Cerca Istruttore", expanded=False):
            col1, col2= st.columns(2)
            
            filtro_cognome = col1.text_input("Cognome Istruttore", placeholder="Inserisci il cognome dell'istruttore")
            
            date_range = col2.date_input(
                "Range data di nascita Istruttore",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            # Gestione dei date input
            try:
                if len(date_range) == 2:
                    start_date, end_date = date_range
                elif len(date_range) == 1:
                    # Se c'è solo una data, usala sia come inizio che come fine
                    start_date = date_range[0]
                    end_date = date_range[0]
                else:
                    # Se non ci sono date selezionate, usa valori predefiniti
                    start_date = min_date
                    end_date = max_date
            except Exception as e:
                # Fallback nel caso di errori
                start_date = min_date
                end_date = max_date
                st.warning("Errore nella selezione delle date. Utilizzato range predefinito.")
        
            
        q_filtro = """ SELECT CodFisc, Nome, Cognome, DataNascita, Email, Telefono FROM Istruttore WHERE 1=1"""
    
        if filtro_cognome:
            q_filtro += f" AND Cognome LIKE '%{filtro_cognome}%'"
            
        q_filtro += f" AND DataNascita BETWEEN '{start_date}' AND '{end_date}'"
        q_filtro += " ORDER BY Cognome, Nome"
        
        istruttori_filtrati = execute_query(st.session_state["connection"], q_filtro)
        df_istruttori_filtrati = pd.DataFrame(istruttori_filtrati)
    
        if df_istruttori_filtrati.empty:
            st.warning("Nessun istruttore corrisponde ai criteri di ricerca.")
            return False
        
        st.caption(f"Trovati {len(df_istruttori_filtrati)} istruttori che corrispondono ai criteri selezionati")
        
        emoji_list = ["👨‍🏫", "👩‍🏫", "🧑‍🏫", "💪", "🏋️", "🤸", "🧘", "🏊", "🚴", "🤾", "⛹️", "🤼", "🏇", "🏄", "🚣"]
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for idx, row in df_istruttori_filtrati.iterrows():
            col_idx = idx % 3
            cod_fisc = row['CodFisc']
            seed = sum(ord(c) for c in cod_fisc)  
            random.seed(seed)
            fixed_emoji = random.choice(emoji_list)
            random.seed()
            
            with cols[col_idx]:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="
                            padding: 15px; 
                            border-radius: 10px; 
                            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                            margin-bottom: 20px;
                            background-color: #f9f9f9;
                        ">
                            <h3 style="text-align: center;">{fixed_emoji} {row['Nome']} {row['Cognome']}</h3>
                            <hr>
                            <p><b>Codice Fiscale:</b> {row['CodFisc']}</p>
                            <p><b>Data di Nascita:</b> {row['DataNascita'].strftime('%d/%m/%Y')}</p>
                            <p><b>Email:</b> {row['Email']}</p>
                            <p><b>Telefono:</b> {row['Telefono'] if pd.notna(row['Telefono']) else 'N/A'}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                # cols = st.columns(2)
                
                # with cols[0]:
                #     st.markdown("### 😀")
                
                # # Dati di ogni istruttore
                # with cols[1]:
                #     st.markdown(f"### {row['Nome']} {row['Cognome']}")
                    
                #     data_nascita = row['DataNascita']
                #     data_nascita_str = data_nascita.strftime('%d/%m/%Y')
                    
                #     st.markdown(f"**Codice Fiscale:** {row['CodFisc']}")
                #     st.markdown(f"**Data di Nascita:** {data_nascita_str}")
                #     st.markdown(f"**Email:** {row['Email']}")
                #     st.markdown(f"**Telefono:** {row['Telefono'] if pd.notna(row['Telefono']) else 'N/A'}")
                # st.markdown("---")
                    
    except Exception as e:
        st.error(f"Errore durante il caricamento degli istruttori: {e}")
        return False
    

if __name__ == "__main__":
    # Configurazione pagina
    st.set_page_config(
        page_title="Istruttori Disponibili",
        layout="wide",
        page_icon="👨",
        initial_sidebar_state="expanded"
    )
    
    st.title("👨 Istruttori Disponibili")
    st.markdown("Visualizza e filtra gli istruttori della palestra")
    
    # Verifica della connessione al database e mostra i dati
    if check_connection():
        show_istruttori_section()

        
        
                