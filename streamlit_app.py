import streamlit as st
from datetime import date
import pandas as pd
from streamlit_gsheets import GSheetsConnection

gSheetsConnection = st.connection("gsheets", type=GSheetsConnection)
df = gSheetsConnection.read(worksheet="Ranking Oficial")
df = df.dropna(how="all")
df = df.sort_values("points", ascending=False).reset_index(drop=True)
top3 = df.head(3)

# Podium list display
sizes = ["32px", "24px", "18px"]
medals = ["🥇", "🥈", "🥉"]

st.subheader("🏆 Top 3 Rankings")

for i in range(3):
    row = top3.iloc[i]
    name = row["blader"]
    points = row["points"]
    image_url = row["avatar"]  # make sure this column exists

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
    st.markdown("---")

# st.set_page_config(page_title="Ranking - OBA", 
#                    page_icon=":shark:"
#                    )

today = str(date.today())

st.title("Organização de Beyblade do Amazonas")
st.write("Última atualização em: " + today)
st.title("RANKING ATUAL")

# # Get the top 3 rows
# top3 = df.head(3)

# # Create three columns (2nd place | 1st place | 3rd place)
# col2, col1, col3 = st.columns([1, 1, 1])  # Left, center, right

# with col2:
#     st.image(top3.iloc[1]['avatar'], width=100)
#     st.markdown(
#         f"<div style='text-align: center;'>"
#         f"<h3>🥈 {top3.iloc[1]['blader']}</h3>"
#         f"<p>{top3.iloc[1]['points']} pontos</p>"
#         f"</div>",
#         unsafe_allow_html=True
#     )

# with col1:
#     st.image(top3.iloc[0]['avatar'], width=100)
#     st.markdown(
#         f"<div style='text-align: center;'>"
#         f"<h1>🥇 {top3.iloc[0]['blader']}</h1>"
#         f"<p style='font-size:20px;'>{top3.iloc[0]['points']} pontos</p>"
#         f"</div>",
#         unsafe_allow_html=True
#     )

# with col3:
#     st.image(top3.iloc[2]['avatar'], width=100)
#     st.markdown(
#         f"<div style='text-align: center;'>"
#         f"<h5>🥉 {top3.iloc[2]['blader']}</h5>"
#         f"<p>{top3.iloc[2]['points']} pontos</p>"
#         f"</div>",
#         unsafe_allow_html=True
#     )

# Spacer / divider
st.markdown("---")
st.subheader("🏅 Demais Colocados")

# Get the rest of the players (starting from index 3)
rest = df.iloc[3:].reset_index(drop=True)

# Option 1: Pretty list with markdown
for i, row in rest.iterrows():
    st.markdown(
        f"**#{i + 4}** — {row['blader']} ({row['points']} pontos)"
    )