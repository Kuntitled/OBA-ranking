import streamlit as st
from datetime import date
from streamlit_gsheets import GSheetsConnection

gSheetsConnection = st.connection("gsheets", type=GSheetsConnection)
df = gSheetsConnection.read()


st.set_page_config(page_title="Ranking - OBA", 
                   page_icon=":shark:"
                   )

today = str(date.today())

st.title("Organização de Beyblade do Amazonas")
st.write(today)
st.title("RANKING ATUAL")

for row in df.itertuples():
    st.write(f"{row.BLADER} tem {row.PONTOS} e está em {row.COLOCAÇÃO}")