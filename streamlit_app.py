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
        image_url = row["avatar"]  # Make sure this column exists in your sheet

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

with tabTwo:
    st.dataframe(df[["blader_id", "blader", "points"]], use_container_width=True)

with tabThree:
    st.title("REGRAS OFICIAIS")
    st.write("------regras vão aqui------")

with tabFour:
    st.subheader("🎖️ Gerador de ID Blader")

    blader_names = df["blader"].tolist()
    selected_name = st.selectbox("Escolha o blader", blader_names)

    if st.button("Gerar Tag"):
        # Get blader info
        row = df[df["blader"] == selected_name].iloc[0]
        name = row["blader"]
        points = row["points"]
        avatar_url = row["avatar"]

        # Create blank background
        tag_img = Image.new("RGB", (300, 500), color="#004488")
        draw = ImageDraw.Draw(tag_img)

        # Load and prepare avatar
        response = requests.get(avatar_url)
        avatar = Image.open(io.BytesIO(response.content)).resize((210, 210)).convert("RGBA")

        # Create circular mask and border
        mask = Image.new("L", (210, 210), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 210, 210), fill=255)

        # Create border circle
        border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border)
        border_draw.ellipse((0, 0, 210, 210), outline="white", width=6)

        # Composite avatar inside border
        avatar_with_alpha = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
        avatar.putalpha(mask)
        avatar_with_alpha.paste(avatar, (0, 0), avatar)
        avatar_with_border = Image.alpha_composite(border, avatar_with_alpha)

        # Paste avatar+border to background
        tag_img.paste(avatar_with_border, (45, 30), avatar_with_border)

        # Load fonts
        title_font = ImageFont.truetype("fonts/Freshman.ttf", 28)
        points_font = ImageFont.truetype("fonts/Freshman.ttf", 20)

        # Centered name
        name_bbox = title_font.getbbox(name)
        name_w = name_bbox[2] - name_bbox[0]
        name_h = name_bbox[3] - name_bbox[1]
        name_x = (tag_img.width - name_w) // 2
        draw.text((name_x, 260), name, font=title_font, fill="white")

        # Centered points
        points_text = f"{points} pontos"
        points_bbox = points_font.getbbox(points_text)
        points_w = points_bbox[2] - points_bbox[0]
        points_h = points_bbox[3] - points_bbox[1]
        points_x = (tag_img.width - points_w) // 2
        draw.text((points_x, 260 + name_h + 10), points_text, font=points_font, fill="white")

        # Show in Streamlit
        st.image(tag_img, caption=f"Tag de {name}")

        # Download button
        buf = io.BytesIO()
        tag_img.save(buf, format="PNG")
        st.download_button(
            label="📥 Baixar Tag",
            data=buf.getvalue(),
            file_name=f"{name}_tag.png",
            mime="image/png"
        )
