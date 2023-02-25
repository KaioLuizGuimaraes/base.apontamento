import streamlit as st
import pyodbc
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import mysql.connector

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected = option_menu(
    menu_title="Menu",
    options=["Home", "Abrir", "Fechar"],
    icons=["list-nested", "check2-circle", "slash-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={

        "icon": {"color": "#CF0210", "font-size": "25px"},
        "nav-link": {
            "font-size": "25px",
            "text-align": "center",
            "margin": "2px",
            "--hover-color": "#A4A6A6",
        },
        "nav-link-selected": {"background-color": "#B4BEC9"},
    },
)

if selected == 'Home':
    components.iframe("https://app.powerbi.com/view?r=eyJrIjoiYTNmYjUzYmQtODA0NC00MDBiLThkZDUtNmFkYzZlMWI0ZjY0IiwidCI6IjQ4YzVhZjk2LTkwZWItNDEyNi04NTJlLThjMTFlMWU2MzBkZCJ9",1600,1000)

if selected == 'Abrir':
    st.title("Abertura de Atividade")
    with st.form(key="lancamento"):
        st.header("Pesquisa")
        input_id = st.text_input(label="Escanear seu Cracha")
        input_atv = st.text_input(label="Escanear Código de Barra da Atividade1")
        input_mot = st.selectbox("Selecione uma opção", ['Iniciar', 'Retrabalho'])
        input_button_submit = st.form_submit_button("Iniciar Atividade")

        if input_button_submit:
            ide = input_id
            atv = input_atv
            motive = input_mot
            conexao = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["user"]
        + ";PWD="
        + st.secrets["password"] )
            cursor = conexao.cursor()
            comando = f"""use Base_cl
                            Insert into info(id, atv, dtini, dtfim, motini, motfim)
                            values(66,99,GETDATE(),0,'teste','Processando')"""
            cursor.execute(comando)
            cursor.commit()
            st.success("Sucesso")

if selected == 'Fechar':
    st.title("Fechamento de Atividade")
    with st.form(key="fechamento"):
        st.header("Insira as informações")
        input_idf = st.text_input(label="Escanear seu Cracha")
        input_atvi = st.text_input(label="Escanear Código de Barra da Atividade1")
        input_mtv = st.selectbox("Selecione uma opção", ['Fim do espediente', 'Parada', 'Retrabalho', 'Finalizado'])
        input_button_submit = st.form_submit_button("Fechar Atividade")

        if input_button_submit:
            idf = input_idf
            avi = input_atvi
            motive = input_mtv
            server = 'PC-13'
            database = 'Base_cl'
            username = 'sa'
            password = 'cl@123'
            cnxn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';ENCRYPT=no;UID=' + username + ';PWD=' + password)
            cursor = cnxn.cursor()
            comando = f"""update info 
                set dtfim = case 
                when id = {idf} and atv = {avi} and motfim = 'Processando' 
                then GETDATE() 
                else dtfim 
                end;
                update info
                set motfim = case
                when id = {idf} and atv = {avi} and dtfim <> 0 and motfim <> 'Finalizado'
                then '{motive}'
                else motfim
                end;"""
            cursor.execute(comando)
            cursor.commit()
            st.success("Sucesso")
