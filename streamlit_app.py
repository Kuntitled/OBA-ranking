import streamlit as st
from datetime import date
import pandas as pd
from streamlit_gsheets import GSheetsConnection

#PAGE CONFIG
st.set_page_config(page_title="Ranking - OBA", page_icon=":shark:")

#GSHEETS CONFIG
gSheetsConnection = st.connection("gsheets", type=GSheetsConnection)
df = gSheetsConnection.read(worksheet="Ranking Oficial")
df = df.dropna(how="all")
df = df.sort_values("points", ascending=False).reset_index(drop=True)
top3 = df.head(3)

today = str(date.today())

# TITLE
st.title("Organização de Beyblade do Amazonas")
st.write("Última atualização em: " + today)
st.title("RANKING ATUAL")

# RANKING
sizes = ["32px", "24px", "18px"]
medals = ["🥇", "🥈", "🥉"]

st.subheader("🏆 Top 3 Bladers")

for i in range(3):
    row = top3.iloc[i]
    name = row["blader"]
    points = row["points"]
    image_url = row["avatar"]

    col_img, col_text = st.columns([1, 4])

    with col_img:
        st.image(image_url, width=60)

    with col_text:
        st.markdown(
            f"<div style='font-size:{sizes[i]}; font-weight:bold;'>"
            f"{medals[i]} {name}</div>"
            f"<div style='font-size:14px; color:gray;'>{points} pontos</div>",
            unsafe_allow_html=True
        )

# OTHER PLACEMENTS
st.markdown("---")
st.subheader("🏅 Demais Colocados")

rest = df.iloc[3:].reset_index(drop=True)

for i, row in rest.iterrows():
    st.markdown(
        f"**#{i + 4}** — {row['blader']} ({row['points']} pontos)"
    )