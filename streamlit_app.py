import streamlit as st
from datetime import date
import requests
import io
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from streamlit_gsheets import GSheetsConnection

# PAGE CONFIG
st.set_page_config(page_title="Ranking - OBA", page_icon=":shark:")
tabOne, tabTwo, tabThree, tabFour = st.tabs(["🏆 Top 10", "📋 Ranking Completo", "✅ Regras", "🐞 Gerar ID Blader"])

# GSHEETS CONFIG
gSheetsConnection = st.connection("gsheets", type=GSheetsConnection)
df = gSheetsConnection.read(worksheet="Ranking Oficial")
df = df.dropna(how="all")
df = df.sort_values("points", ascending=False).reset_index(drop=True)
top3 = df.head(3)

today = str(date.today())
with tabOne:
    # TITLE
    st.title("Organização de Beyblade do Amazonas")
    st.write("Última atualização em: " + today)
    st.title("RANKING ATUAL")

    # RANKING - TOP 3
    sizes = ["32px", "24px", "18px"]
    medals = ["🥇", "🥈", "🥉"]

    st.subheader("🏆 Top 3 Bladers")

    for i in range(3):
        row = top3.iloc[i]
        name = row["blader"]
        points = row["points"]
        image_url = row["avatar"] 

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <img src="{image_url}" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 15px;">
                <div>
                    <div style="font-size: {sizes[i]}; font-weight: bold;">{medals[i]} {name}</div>
                    <div style="font-size: 14px; color: gray;">{points} pontos</div>
                </div>
            </div>
            <hr>
            """,
            unsafe_allow_html=True
        )

    # OTHER PLACEMENTS
    st.subheader("🏅 Demais Colocados:")
    rest = df.iloc[3:].reset_index(drop=True)

    for i, row in rest.iterrows():
        st.markdown(
            f"**#{i + 4}** — {row['blader']} ({row['points']} pontos)"
        )

    # DIVIDER
    st.markdown("---")

    # SOCIAL MEDIA
    st.markdown(
        """
        <div style="text-align: center; font-size: 16px;">
            📱 Siga a <strong>OBA</strong> nas redes sociais:<br>
            <a href="https://www.instagram.com/beybladeamazonas?igsh=MWkwbTZ5OW56am80Mw==" target="_blank">Instagram</a> |
            <a href="https://www.tiktok.com/@beybladexbatalha?_t=ZM-8vWyk4NNFPr&_r=1" target="_blank">TikTok</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with tabTwo: # ABA TABELA COMPLETA
    st.dataframe(
    df[["blader_id", "blader", "points", "matches", "wins", "losses", "win_loss_ratio"]]
    .rename(columns={
        "blader_id": "ID",
        "blader": "Nome",
        "points": "Pontos",
        "matches": "Partidas",
        "wins": "Vitórias",
        "losses": "Derrotas",
        "win_loss_ratio": "Taxa V/D"
    }),
    use_container_width=True
)

with tabThree: # ABA REGRAS
    st.title("REGRAS OFICIAIS")
    st.write("------regras vão aqui------")

with tabFour: # ABA GERADOR ID BLADER
    st.subheader("🎖️ Gerador de ID Blader")

    blader_names = df["blader"].tolist()
    selected_name = st.selectbox("Escolha o blader", blader_names)

    if st.button("Gerar Tag"):
        # INFORMAÇÃO BLADER
        row = df[df["blader"] == selected_name].iloc[0]
        name = row["blader"]
        points = row["points"]
        avatar_url = row["avatar"]

        # FUNDO
        
        tag_img = Image.new("RGB", (300, 500), color="black")
        draw = ImageDraw.Draw(tag_img)

        # LISTRA
        stripe_width = 60
        stripe_x = (tag_img.width - stripe_width) // 2
        draw.rectangle([stripe_x, 0, stripe_x + stripe_width, tag_img.height], fill="red")

        # TÍTULO
        header_font = ImageFont.truetype("fonts/MASQUE.ttf", 14) 
        header_text = "ORGANIZAÇÃO DE BEYBLADE DO AMAZONAS"
        header_w, header_h = draw.textbbox((0, 0), header_text, font=header_font)[2:]
        header_x = (tag_img.width - header_w) // 2
        draw.text((header_x, 10), header_text, font=header_font, fill="white")

        # AVATAR
        response = requests.get(avatar_url)
        avatar = Image.open(io.BytesIO(response.content)).resize((210, 210)).convert("RGBA")

        # MARCAÇÃO E BORDA
        mask = Image.new("L", (210, 210), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 210, 210), fill=255)

        # BORDA CIRCULAR
        border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border)
        border_draw.ellipse((0, 0, 210, 210), outline="white", width=6)

        # AVATAR 
        avatar_with_alpha = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
        avatar.putalpha(mask)
        avatar_with_alpha.paste(avatar, (0, 0), avatar)
        avatar_with_border = Image.alpha_composite(border, avatar_with_alpha)

        # AVATAR
        tag_img.paste(avatar_with_border, (50, 40 + header_h), avatar_with_border)

        # CARREGAR FONTE
        title_font = ImageFont.truetype("fonts/Freshman.ttf", 28)
        points_font = ImageFont.truetype("fonts/Freshman.ttf", 20)

        # NOME CENTRALIZADO
        name_bbox = title_font.getbbox(name)
        name_w = name_bbox[2] - name_bbox[0]
        name_h = name_bbox[3] - name_bbox[1]
        name_x = (tag_img.width - name_w) // 2
        draw.text((name_x, 270), name, font=title_font, fill="white")

        # PONTO CENTRALIZADO
        points_text = f"{points} pontos"
        points_bbox = points_font.getbbox(points_text)
        points_w = points_bbox[2] - points_bbox[0]
        points_h = points_bbox[3] - points_bbox[1]
        points_x = (tag_img.width - points_w) // 2
        draw.text((points_x, 270 + name_h + 10), points_text, font=points_font, fill="white")

        # MOSTRAR
        st.image(tag_img, caption=f"Tag de {name}")

        # BOTÃO DOWNLOAD
        buf = io.BytesIO()
        tag_img.save(buf, format="PNG")
        st.download_button(
            label="📥 Baixar Tag",
            data=buf.getvalue(),
            file_name=f"{name}_tag.png",
            mime="image/png"
        )
