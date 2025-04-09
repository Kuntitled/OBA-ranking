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

for row in df.itertuples()[:3]:
    st.write(f"{row.blader} tem {row.points} e está em {row.placement}")