import streamlit as st
from datetime import date


today = str(date.today())

st.title("Organização de Beyblade do Amazonas " + today )
st.title("RANKING ATUAL")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
