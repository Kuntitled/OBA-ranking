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
    # st.markdown(
    #     """
    # 🏆 **Torneio Oficial Beyblade Amazonas** — 1×1 até 4 Pontos

    # 📅 **Data e Horários**  
    # - **Início:** 14h (tolerância de 30 min)  
    # - **Local:** Ponta Negra, Manaus  

    # 📋 **Formato & Regras**  
    # - Confrontos 1×1, vitória aos 4 pontos.  
    # - Somente peças **originais** de Beyblade; peças “fake” são proibidas.  
    # - **Wizard Rod** banido. Sem mais outras restrições de peças.  
    # - ❗ Qualquer infração resulta em **desclassificação imediata**.  

    # 🎖 **Premiação**  
    # - 🥇 **1º lugar:** Beyblade + medalha  
    # - 🥈 **2º lugar:** Beyblade + medalha  
    # - 🥉 **3º lugar:** Medalha  

    # 💰 **Inscrições**  
    # 1. **1º lote:** R\$ 20 (01/05 ▶ 09/05)  
    # 2. **2º lote:** R\$ 25 (10/05 ▶ 17/05)  
    # 3. **3º lote:** R\$ 30 (a partir de 18/05)  

    # ✔️ Após a confirmação do pagamento, você receberá um link para cadastro no **Ranking Oficial**.  

    # 🚨 **Não perca!** Garanta já sua vaga e prepare-se para a batalha! 🚨
    #         """,
    #     unsafe_allow_html=True
    # )
    # st.markdown("---")
    # st.write("Pix da inscrição:")
    # st.write("92 99999-3714")
    # st.write("Carlos Francisco Bussons do Vale")
    # st.write("Nubank")
    # st.write("CLIQUE NO BOTÃO PARA ENTRAR EM CONTATO PARA SE INSCREVER E ENVIAR O COMPROVANTE DO PIX")
    # if st.button("🟢 WhatsApp"):
    #     st.write("[Abrir chat](https://wa.me/559299993714?text=Ol%C3%A1%2C%20quero%20me%20inscrever%20no%20torneio%21)")

    st.markdown("---")
    st.write("Mais informações em breve!")
    st.write("Nos acompanhe nas redes sociais!")

with tabFour: # ABA REGRAS
    st.title("REGRAS OFICIAIS")
    st.write("------regras vão aqui------")

with tabFive:  # ABA GERADOR ID BLADER
    st.subheader("🎖️ Gerador de ID Blader")

    # 1) Input blader_id as zero-padded 3‑digit string
    input_id = st.text_input(
        "Digite seu ID de Blader (3 dígitos, ex: 001)",
        value="001",
        max_chars=3
    )

    if st.button("Gerar Tag"):
        # 2) Prepare ID column for lookup
        df["blader_id_str"] = df["blader_id"].astype(int).astype(str).str.zfill(3)

        if input_id not in df["blader_id_str"].values:
            st.error(f"ID {input_id} não encontrado. Verifique e tente novamente.")
        else:
            # 3) Fetch row by ID
            row = df[df["blader_id_str"] == input_id].iloc[0]
            name = row["blader"]
            points = row["points"]
            avatar_url = row["avatar"]
            blader_id = input_id

            # 4) Create base tag (300×500 px)
            tag_img = Image.new("RGB", (300, 500), color="black")
            draw = ImageDraw.Draw(tag_img)

            # 5) Red stripe center
            stripe_w = 60
            stripe_x = (tag_img.width - stripe_w) // 2
            draw.rectangle([stripe_x, 0, stripe_x + stripe_w, tag_img.height], fill="red")

            # 6) Header (two centered lines)
            header_font = ImageFont.truetype("fonts/MASQUE.ttf", 14)
            header_lines = ["ORGANIZAÇÃO DE", "BEYBLADE DO AMAZONAS"]
            header_y = 10
            for line in header_lines:
                bbox = draw.textbbox((0, 0), line, font=header_font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                x = (tag_img.width - w) // 2
                draw.text((x, header_y), line, font=header_font, fill="white")
                header_y += h + 2

            # 7) Avatar with circular mask + white border
            resp = requests.get(avatar_url)
            avatar = Image.open(io.BytesIO(resp.content)).resize((210, 210)).convert("RGBA")
            mask = Image.new("L", (210, 210), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 210, 210), fill=255)
            border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
            ImageDraw.Draw(border).ellipse((0, 0, 210, 210), outline="white", width=6)
            avatar.putalpha(mask)
            laid = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
            laid.paste(avatar, (0, 0), avatar)
            avatar_with_border = Image.alpha_composite(border, laid)
            avatar_y = header_y + 10
            tag_img.paste(avatar_with_border, (45, avatar_y), avatar_with_border)

            # 8) Fonts for ID, name, points, stats
            id_font     = ImageFont.truetype("fonts/Freshman.ttf", 18)
            name_font   = ImageFont.truetype("fonts/American Captain.ttf", 36)
            points_font = ImageFont.truetype("fonts/American Captain.ttf", 32)
            stats_font  = ImageFont.truetype("fonts/American Captain.ttf", 24)

            # 9) Draw ID (#001) centered below avatar
            id_text = f"#{blader_id}"
            bbox = id_font.getbbox(id_text)
            x = (tag_img.width - (bbox[2]-bbox[0])) // 2
            y = avatar_y + 210 + 15
            draw.text((x, y), id_text, font=id_font, fill="white")

            # 10) Draw name
            name_y = y + (bbox[3]-bbox[1]) + 15
            bbox = name_font.getbbox(name)
            x = (tag_img.width - (bbox[2]-bbox[0])) // 2
            draw.text((x, name_y), name, font=name_font, fill="white")

            # 11) Draw points (integer)
            pts_text = f"{int(points)} pontos"
            pts_y = name_y + (bbox[3]-bbox[1]) + 20
            bbox = points_font.getbbox(pts_text)
            x = (tag_img.width - (bbox[2]-bbox[0])) // 2
            draw.text((x, pts_y), pts_text, font=points_font, fill="white")

            # 12) Draw stats (wins/losses/ratio)
            wins, losses = int(row.get("wins", 0)), int(row.get("losses", 0))
            ratio = float(row.get("win_loss_ratio", 0))
            stats = [f"Vitórias: {wins}", f"Derrotas: {losses}", f"V/D: {ratio:.2f}"]
            stats_y = pts_y + (bbox[3]-bbox[1]) + 50
            for line in stats:
                bbox = stats_font.getbbox(line)
                x = (tag_img.width - (bbox[2]-bbox[0])) // 2
                draw.text((x, stats_y), line, font=stats_font, fill="white")
                stats_y += (bbox[3]-bbox[1]) + 5

            # 13) Upscale 2x for higher resolution download
            high_res = tag_img.resize((600, 1000), resample=Image.LANCZOS)

            # 14) Display and download
            st.image(high_res, caption=f"Tag de {name}")
            buf = io.BytesIO()
            high_res.save(buf, format="PNG")
            st.download_button(
                "📥 Baixar Tag",
                data=buf.getvalue(),
                file_name=f"{blader_id}_{name}_tag.png",
                mime="image/png"
            )
