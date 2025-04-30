import streamlit as st
from datetime import date
import requests
import io
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from streamlit_gsheets import GSheetsConnection

# PAGE CONFIG
st.set_page_config(page_title="Ranking - OBA", page_icon=":shark:")
tabOne, tabTwo, tabThree, tabFour, tabFive = st.tabs(["🏆 Top 10", "📋 Ranking Completo", "🗓️ Próximo Evento", "✅ Regras", "🐞 Gerar Blader Tag"])

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
    st.markdown("""
    ## ⚙️ Componentes de Jogo — Regras Oficiais OBA

    ### 🌀 Beyblade (Bey)  
    O <strong>Bey</strong> (ou <em>Beyblade</em>) é o pião utilizado nas batalhas.  
    • Cada Blader deve possuir <strong>pelo menos um Bey completo</strong> para participar de uma batalha.  
    • Um Bey completo é composto por: <strong>Blade</strong>, <strong>Ratchet</strong> e <strong>Bit</strong>.  
    • No sistema CX, o <strong>Blade</strong> deve conter as <strong>três partes obrigatórias</strong>:  
     ◦ <em>Lock Chip</em>  
     ◦ <em>Lâmina Principal (Main Blade)</em>  
     ◦ <em>Lâmina Auxiliar (Assist Blade)</em>  

    ---

    ### 📦 Deck  
    Um <em>deck</em> é um conjunto de <strong>3 Beys</strong>, exigido em certos formatos de partida.  
    • Cada deck pode conter <strong>apenas uma cópia de cada peça</strong>, com exceção dos <em>Lock Chips</em>, que podem ser repetidos.  
    • Peças com <strong>o mesmo nome</strong> são consideradas a mesma peça, mesmo com variações regionais no nome.  
     ◦ Ex: <em>Phoenix Wing</em> e <em>Soar Phoenix</em> são tratadas como a mesma peça.  
    • Peças com <strong>design diferente</strong>, mas nomes distintos, são consideradas <strong>peças únicas</strong>.  
     ◦ Ex: <em>Roar Tyranno</em> ≠ <em>Soar Phoenix</em>.  
    • Variações de tipo com o mesmo nome (ex: <em>Lightning L-Drago</em> tipo “upper” e tipo “rapid-hit”) são consideradas a <strong>mesma peça</strong>.  
    • <strong>Não é permitido trocar peças entre os Beys do deck durante uma partida.</strong>

    ---

    ### 🚀 Lançador (Launcher)  
    O lançador é o dispositivo utilizado para lançar o Bey na arena.  
    • Existem dois tipos:  
     ◦ <strong>String Launcher</strong> (com mecanismo interno de corda)  
     ◦ <strong>Winder Launcher</strong> (com corda manual externa)  
    • <strong>Qualquer acessório conectado ao lançador</strong> é considerado parte oficial do lançador e está sujeito às mesmas regras.
    """, unsafe_allow_html=True)

    st.markdown("---") # DIVISOR

    st.markdown("""
    ## 🏟️ Estádio — Regras Oficiais OBA

    As batalhas acontecem dentro do <strong>estádio</strong>, que é composto por duas partes principais:  

    • <strong>Tampa do Estádio (Stadium Cover)</strong>: inclui a área de lançamento — uma abertura circular por onde os Beys são lançados.  
    • <strong>Corpo do Estádio (Stadium Body)</strong>: é a superfície onde os Beys batalham.  

    ---

    ### ⚔️ Zonas do Estádio  

    O espaço interno do estádio (entre a tampa e o corpo) é dividido em três zonas que influenciam diretamente a batalha:

    🔵 <strong>Zona de Batalha (Battle Zone)</strong>  
    – Abrange <em>toda a área interna</em> do estádio, <strong>exceto</strong> as zonas Over e Xtreme.  
    – É o espaço principal onde os Beys giram e se enfrentam.  

    🕳️ <strong>Zona Over (Over Zone)</strong>  
    – São dois bolsões localizados nos <strong>cantos esquerdo e direito da frente</strong> do estádio.  
    – Um Bey que cai aqui pode ser considerado fora de jogo, dependendo das regras do formato.  

    🚨 <strong>Zona Xtreme (Xtreme Zone)</strong>  
    – É a grande abertura localizada na <strong>parte frontal central</strong> do estádio.  
    – Beys que saem por essa abertura normalmente resultam em pontos de vitória para o oponente.  


    🔎 Um Bey é considerado dentro de uma zona assim que a <strong>maior parte de sua estrutura</strong> estiver dentro da respectiva área.
    """, unsafe_allow_html=True)

    st.markdown("---") # DIVISOR

    st.markdown("""
    ## ⚔️ DUELO OFICIAL – OBA (Organização de Beyblade do Amazonas)

    1. 🔊 **Anúncio do Duelo**  
    Todo duelo oficial deve ser **anunciado verbalmente**, seja **presencialmente** ou por **mensagem no grupo oficial**, por um dos desafiantes.

    2. ✅ **Aceitação do Adversário**  
    O adversário deve **aceitar o desafio verbalmente**, também de forma presencial ou no grupo oficial.

    3. 📋 **Definição de Regras**  
    A dupla de duelistas deve **entrar em consenso** sobre as regras que serão utilizadas. Todas as **regras oficiais disponíveis** podem ser escolhidas para compor o formato do duelo.

    4. 🧑‍⚖️ **Comunicação com a Organização**  
    Após o acordo, o duelo precisa ser **comunicado a um Representante Oficial da OBA**, que avaliará e aprovará a solicitação.

    5. 📅 **Agendamento**  
    Com o duelo aprovado por um Oficial, será marcado um **local e horário** para sua realização.

    6. 🏆 **Registro Oficial**  
    Todos os duelos oficiais, assim como suas **vitórias e derrotas**, serão **registrados no Ranking Oficial** e farão parte do **histórico oficial de partidas** da organização.

    7. 📜 **Consulta de Regras**  
    As regras utilizadas no duelo deverão ser aquelas disponíveis na aba **“📜 Regras Oficiais”**.
    """)


with tabFive:  # ABA GERADOR BLADER TAG
    st.subheader("🎖️ Gerador de Blader Tag")

    # INPUT DO ID BLADER
    input_id = st.text_input(
        "Digite seu ID de Blader (3 dígitos, ex: 001)",
        value="005",
        max_chars=3
    )

    if st.button("Gerar Tag"):
        # PESQUISAR ID
        df["blader_id_str"] = df["blader_id"].astype(int).astype(str).str.zfill(3)

        if input_id not in df["blader_id_str"].values:
            st.error(f"ID {input_id} não encontrado. Verifique e tente novamente.")
        else:
            # PUXAR ID
            row = df[df["blader_id_str"] == input_id].iloc[0]
            name = row["blader"]
            points = row["points"]
            avatar_url = row["avatar"]
            blader_id = input_id

            # TAG BASE
            tag_img = Image.new("RGB", (300, 500), color="black")
            draw = ImageDraw.Draw(tag_img)

            # LISTRA VERMELHA
            stripe_w = 60
            stripe_x = (tag_img.width - stripe_w) // 2
            draw.rectangle([stripe_x, 0, stripe_x + stripe_w, tag_img.height], fill="red")

            # CABEÇALHO
            header_font = ImageFont.truetype("fonts/MASQUE.ttf", 14)
            header_lines = ["ORGANIZAÇÃO DE", "BEYBLADE DO AMAZONAS"]
            header_y = 10
            for line in header_lines:
                bbox = draw.textbbox((0, 0), line, font=header_font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                x = (tag_img.width - w) // 2
                draw.text((x, header_y), line, font=header_font, fill="white")
                header_y += h + 2

            # AVATAR E BORDA
            resp = requests.get(avatar_url)
            avatar = Image.open(io.BytesIO(resp.content)).resize((210, 210)).convert("RGBA")
            mask = Image.new("L", (210, 210), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 210, 210), fill=255)
            border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
            ImageDraw.Draw(border).ellipse((0, 0, 210, 210), outline="white", width=12) #LARGURA BORDA
            avatar.putalpha(mask)
            laid = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
            laid.paste(avatar, (0, 0), avatar)
            avatar_with_border = Image.alpha_composite(border, laid)
            avatar_y = header_y + 10
            tag_img.paste(avatar_with_border, (45, avatar_y), avatar_with_border)

            # FONTES
            id_font     = ImageFont.truetype("fonts/Freshman.ttf", 18)
            name_font   = ImageFont.truetype("fonts/American Captain.ttf", 36)
            points_font = ImageFont.truetype("fonts/American Captain.ttf", 32)
            stats_font  = ImageFont.truetype("fonts/American Captain.ttf", 24)

            # BLADER ID
            id_text = f"#{blader_id}"
            bbox = id_font.getbbox(id_text)
            x = (tag_img.width - (bbox[2]-bbox[0])) // 2
            y = avatar_y + 210 + 15
            draw.text((x, y), id_text, font=id_font, fill="white")

            # NOME
            name_y = y + (bbox[3]-bbox[1]) + 15
            bbox = name_font.getbbox(name)
            x = (tag_img.width - (bbox[2]-bbox[0])) // 2
            draw.text((x, name_y), name, font=name_font, fill="white")

            # PONTOS
            pts_text = f"{int(points)} pontos"
            pts_y = name_y + (bbox[3]-bbox[1]) + 25
            bbox = points_font.getbbox(pts_text)
            x = (tag_img.width - (bbox[2]-bbox[0])) // 2
            draw.text((x, pts_y), pts_text, font=points_font, fill="white")

            # ESTATÍSTICAS
            wins, losses = int(row.get("wins", 0)), int(row.get("losses", 0))
            ratio = float(row.get("win_loss_ratio", 0))
            stats = [f"Vitorias: {wins}", f"Derrotas: {losses}", f"V/D: {ratio:.2f}"]
            stats_y = pts_y + (bbox[3]-bbox[1]) + 40
            for line in stats:
                bbox = stats_font.getbbox(line)
                x = (tag_img.width - (bbox[2]-bbox[0])) // 2
                draw.text((x, stats_y), line, font=stats_font, fill="white")
                stats_y += (bbox[3]-bbox[1]) + 5

            # UPSCALE
            high_res = tag_img.resize((600, 1000), resample=Image.LANCZOS)

            # MOSTRAR E BAIXAR
            st.image(high_res, caption=f"Tag de {name}")
            buf = io.BytesIO()
            high_res.save(buf, format="PNG")
            st.download_button(
                "📥 Baixar Tag",
                data=buf.getvalue(),
                file_name=f"{blader_id}_{name}_tag.png",
                mime="image/png"
            )
