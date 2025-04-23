import streamlit as st
from datetime import date
import requests
import io
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from streamlit_gsheets import GSheetsConnection

# PAGE CONFIG
st.set_page_config(page_title="Ranking - OBA", page_icon=":shark:")
tabOne, tabTwo, tabThree, tabFour, tabFive = st.tabs(["🏆 Top 10", "📋 Ranking Completo", "🗓️ Próximo Evento", "✅ Regras", "🐞 Gerar ID Blader"])

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
        points = int(row["points"])
        image_url = row["avatar"]
        id_top10 = int(row["blader_id"])
        id_str_top10 = str(id_top10).zfill(3)
         

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <img src="{image_url}" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 15px;">
                <div>
                    <div style="font-size: {sizes[i]}; font-weight: bold;">{medals[i]} #{id_str_top10} {name}</div>
                    <div style="font-size: 14px; color: gray;">{points} pontos</div>
                </div>
            </div>
            <hr>
            """,
            unsafe_allow_html=True
        )

    # OTHER PLACEMENTS
    st.subheader("🏅 Demais Colocados:")
    #rest = df.iloc[3:].reset_index(drop=True)
    rest = df.iloc[3:10].reset_index(drop=True)

    for i, row in rest.iterrows():
        st.markdown(
            f"**#{i + 4}** — #{str(int(row['blader_id'])).zfill(3)} {row['blader']} ({int(row['points'])} pontos)"
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
    df["blader_id"] = df["blader_id"].astype(int).astype(str).str.zfill(3)
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

with tabThree: # ABA EVENTOS
    st.title("REGRAS & DETALHES DO PRÓXIMO TORNEIO")
    st.markdown(
        """
    🏆 **Torneio Oficial Beyblade Amazonas** — 1×1 até 4 Pontos

    📅 **Data e Horários**  
    - **Início:** 14h (tolerância de 30 min)  
    - **Local:** Ponta Negra, Manaus  

    📋 **Formato & Regras**  
    - Confrontos 1×1, vitória aos 4 pontos.  
    - Somente peças **originais** de Beyblade; peças “fake” são proibidas.  
    - **Wizard Rod** banido. Sem mais outras restrições de peças.  
    - ❗ Qualquer infração resulta em **desclassificação imediata**.  

    🎖 **Premiação**  
    - 🥇 **1º lugar:** Beyblade + medalha  
    - 🥈 **2º lugar:** Beyblade + medalha  
    - 🥉 **3º lugar:** Medalha  

    💰 **Inscrições**  
    1. **1º lote:** R\$ 20 (01/05 ▶ 09/05)  
    2. **2º lote:** R\$ 25 (10/05 ▶ 17/05)  
    3. **3º lote:** R\$ 30 (a partir de 18/05)  

    ✔️ Após a confirmação do pagamento, você receberá um link para cadastro no **Ranking Oficial**.  

    🚨 **Não perca!** Garanta já sua vaga e prepare-se para a batalha! 🚨
            """,
        unsafe_allow_html=True
    )
    if st.button("🟢 WhatsApp"):
        st.write("[Abrir chat](https://wa.me/559299993714v?text=Ol%C3%A1%2C%20quero%20me%20inscrever%20no%20torneio%21)")


with tabFour: # ABA REGRAS
    st.title("REGRAS OFICIAIS")
    st.write("------regras vão aqui------")

with tabFive:  # ABA GERADOR ID BLADER
    st.subheader("🎖️ Gerador de ID Blader")

    blader_names = df["blader"].tolist()
    selected_name = st.selectbox("Escolha o blader", blader_names)

    if st.button("Gerar Tag"):
        # INFORMAÇÃO BLADER
        row = df[df["blader"] == selected_name].iloc[0]
        name = row["blader"]
        points = row["points"]
        avatar_url = row["avatar"]
        blader_id = str(int(row["blader_id"])).zfill(3)

        # FUNDO
        tag_img = Image.new("RGB", (300, 500), color="black")
        draw = ImageDraw.Draw(tag_img)

        # LISTRA VERMELHA
        stripe_width = 60
        stripe_x = (tag_img.width - stripe_width) // 2
        draw.rectangle([stripe_x, 0, stripe_x + stripe_width, tag_img.height], fill="red")

        # TÍTULO (duas linhas centralizadas)
        header_font = ImageFont.truetype("fonts/MASQUE.ttf", 14)
        header_lines = ["ORGANIZAÇÃO DE", "BEYBLADE DO AMAZONAS"]
        header_y = 10

        for line in header_lines:
            line_bbox = draw.textbbox((0, 0), line, font=header_font)
            line_w = line_bbox[2] - line_bbox[0]
            line_h = line_bbox[3] - line_bbox[1]
            line_x = (tag_img.width - line_w) // 2
            draw.text((line_x, header_y), line, font=header_font, fill="white")
            header_y += line_h + 2  # move down for next line

        # AVATAR
        response = requests.get(avatar_url)
        avatar = Image.open(io.BytesIO(response.content)).resize((210, 210)).convert("RGBA")

        # MÁSCARA E BORDA CIRCULAR
        mask = Image.new("L", (210, 210), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 210, 210), fill=255)

        border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border)
        border_draw.ellipse((0, 0, 210, 210), outline="white", width=6)
        avatar_with_alpha = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
        avatar.putalpha(mask)
        avatar_with_alpha.paste(avatar, (0, 0), avatar)
        avatar_with_border = Image.alpha_composite(border, avatar_with_alpha)

        avatar_y = header_y + 10
        tag_img.paste(avatar_with_border, (45, avatar_y), avatar_with_border)

        # FONTES
        title_font = ImageFont.truetype("fonts/American Captain.ttf", 36)
        points_font = ImageFont.truetype("fonts/American Captain.ttf", 32)
        id_font = ImageFont.truetype("fonts/Freshman.ttf", 18)
        stats_font = ImageFont.truetype("fonts/American Captain.ttf", 24)

        # ID CENTRALIZADO ABAIXO DO AVATAR
        id_text = f"#{blader_id}"
        id_bbox = id_font.getbbox(id_text)
        id_w = id_bbox[2] - id_bbox[0]
        id_h = id_bbox[3] - id_bbox[1]
        id_x = (tag_img.width - id_w) // 2
        id_y = avatar_y + 210 + 15
        draw.text((id_x, id_y), id_text, font=id_font, fill="white")

        # NOME CENTRALIZADO
        name_y = id_y + id_h + 20
        name_bbox = title_font.getbbox(name)
        name_w = name_bbox[2] - name_bbox[0]
        name_h = name_bbox[3] - name_bbox[1]
        name_x = (tag_img.width - name_w) // 2
        draw.text((name_x, name_y), name, font=title_font, fill="white")

        # PONTOS CENTRALIZADOS
        points_text = f"{int(points)} pontos"
        points_y = name_y + name_h + 20
        points_bbox = points_font.getbbox(points_text)
        points_w = points_bbox[2] - points_bbox[0]
        points_x = (tag_img.width - points_w) // 2
        draw.text((points_x, points_y), points_text, font=points_font, fill="white")

        # ESTATÍSTICAS (V/D/R)
        wins = int(row.get("wins", 0))
        losses = int(row.get("losses", 0))
        ratio = float(row.get("win_loss_ratio", 0))
        ratio_str = f"{ratio:.2f}"

        stats_y = points_y + 50  # espaçamento abaixo dos pontos
        stat_lines = [
            f"Vitorias: {wins}",
            f"Derrotas: {losses}",
            f"V/D: {ratio_str}"
        ]

        for line in stat_lines:
            line_bbox = stats_font.getbbox(line)
            line_w = line_bbox[2] - line_bbox[0]
            line_x = (tag_img.width - line_w) // 2
            draw.text((line_x, stats_y), line, font=stats_font, fill="white")
            stats_y += 25  # espaçamento entre linhas

        # MOSTRAR
        st.image(tag_img, caption=f"Tag de {name}")
        high_res_tag = tag_img.resize((600, 1000), resample=Image.LANCZOS)

        # BOTÃO DOWNLOAD
        buf = io.BytesIO()
        high_res_tag.save(buf, format="PNG")
        st.download_button(
            label="📥 Baixar Tag",
            data=buf.getvalue(),
            file_name=f"{name}_tag.png",
            mime="image/png"
        )
