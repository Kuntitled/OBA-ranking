import streamlit as st
from datetime import date
import requests
import io
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from streamlit_gsheets import GSheetsConnection

# PAGE CONFIG
st.set_page_config(page_title="Organização de Beyblade do Amazonas", page_icon=":shark:")
tabOne, tabDuels, tabRegras, tabTwo, tabSix = st.tabs(["🏆 Top 10", "🏅 Top 10 Duelistas","🧩 Regras", "✅ Ranking Completo", "🐞 Gerar Blader Tag"])

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

    # Ensure numeric values
    df["points"] = pd.to_numeric(df["points"], errors="coerce").fillna(0)
    df["wins"] = pd.to_numeric(df["wins"], errors="coerce").fillna(0)
    df["losses"] = pd.to_numeric(df["losses"], errors="coerce").fillna(0)

    # Calculate win rate
    df["win_rate"] = df.apply(
        lambda r: (r["wins"] / (r["wins"] + r["losses"]) * 100)
        if (r["wins"] + r["losses"]) > 0 else 0,
        axis=1
    )

    # Sort: points → wins → win_rate → fewer losses
    df = df.sort_values(
        by=["points", "wins", "win_rate", "losses"],
        ascending=[False, False, False, True]
    ).reset_index(drop=True)

    # RANKING - TOP 3
    sizes = ["32px", "24px", "18px"]
    medals = ["🥇", "🥈", "🥉"]

    st.subheader("🏆 Top 3 Bladers")

    for i in range(3):
        row = df.iloc[i]
        name = row["blader"]
        points = int(row["points"])
        wins = int(row.get("wins", 0))
        losses = int(row.get("losses", 0))
        win_rate = row["win_rate"]
        image_url = row["avatar"]
        id_str = str(int(row["blader_id"])).zfill(3)

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <img src="{image_url}" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 15px;">
                <div>
                    <div style="font-size: {sizes[i]}; font-weight: bold;">{medals[i]} #{id_str} {name}</div>
                    <div style="font-size: 14px; color: gray;">{points} pontos</div>
                    <div style="font-size: 13px; color: gray;">
                        Vitórias: {wins} | Derrotas: {losses} | Taxa de Vitória: {win_rate:.1f}%
                    </div>
                </div>
            </div>
            <hr>
            """,
            unsafe_allow_html=True
        )

    # OTHER PLACEMENTS (Top 4–16)
    st.subheader("🏅 Demais Colocados:")
    rest = df.iloc[3:16].reset_index(drop=True)  # 🔥 now showing places 4 to 16

    for i, row in rest.iterrows():
        id_str = str(int(row['blader_id'])).zfill(3)
        wins = int(row.get("wins", 0))
        losses = int(row.get("losses", 0))
        win_rate = row["win_rate"]

        st.markdown(
            f"""**#{i + 4}** — #{id_str} {row['blader']} ({int(row['points'])} pontos)  
            🟢 Vitórias: {wins} | 🔴 Derrotas: {losses} | 🎯 Taxa: {win_rate:.1f}%"""
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


with tabDuels:
    min_duels = 5
    top_win_rate = df[df["duels"] >= min_duels].copy()
    top_win_rate["duel_win_loss_percentage"] = (top_win_rate["duel_win_loss_percentage"] * 100).round(1)
    top_win_rate = top_win_rate.sort_values(by="duel_win_loss_percentage", ascending=False).head(10)

    top_duel_wins = df.sort_values(by="duel_win", ascending=False).head(10)

    def render_leaderboard(title, data, metric_col, percentage=False):
        st.markdown(f"## {title}")
        bg_colors = ["#d4af37", "#c0c0c0", "#cd7f32"]  # Gold, Silver, Bronze

        for rank, (_, row) in enumerate(data.iterrows()):
            cols = st.columns([1, 4])
            with cols[0]:
                st.markdown(
                    f"<img src='{row['avatar']}' width='60' style='border-radius: 50%; object-fit: cover;'/>",
                    unsafe_allow_html=True
                )
            with cols[1]:
                name_size = "24px" if rank < 3 else "16px"
                bg_style = f"background-color:{bg_colors[rank]}; padding:10px; border-radius:10px;" if rank < 3 else ""
                metric = f'{row[metric_col]:.1f}%' if percentage else int(row[metric_col])

                st.markdown( 
                    f"""
                    <div style="{bg_style}">
                        <div style="font-size:{name_size}; font-weight:bold;">
                            #{int(row['blader_id']):03d} - {row['blader']}
                        </div>
                        <div style="color:white;">
                            Vitórias: {metric}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    render_leaderboard("🏆 Top 10 por Porcentagem de Vitórias em Duelos", top_win_rate, "duel_win_loss_percentage", percentage=True)
    render_leaderboard("🔥 Top 10 por Número de Vitórias em Duelos", top_duel_wins, "duel_win")

with tabRegras:
    st.markdown("""
# 🌀 Regras Oficiais OBA

---

## 🧩 Componentes de Jogo

### 🌪️ Beyblade (Bey)
- O Bey (ou Beyblade) é o pião utilizado nas batalhas.  
- Cada Blader deve possuir pelo menos um Bey completo para participar de uma batalha.  
- Um Bey completo é composto por: **Blade**, **Ratchet** e **Bit**.  
- No sistema CX, o Blade deve conter as três partes obrigatórias:  
  - 🔒 Lock Chip  
  - ⚔️ Lâmina Principal (Main Blade)  
  - 🛡️ Lâmina Auxiliar (Assist Blade)

---

### 📦 Deck
- Um deck é um conjunto de **3 Beys**, exigido em certos formatos de partida.  
- Cada deck pode conter apenas **uma cópia de cada peça**, com exceção dos **Lock Chips**, que podem ser repetidos (Lock Chips com metal são limitados a uma unidade por deck).  
- O deck poderá conter um **4º combo reserva** para trocas apenas entre batalhas.  
- Peças com o mesmo nome são consideradas iguais, mesmo com variações regionais.  
  - Ex: *Phoenix Wing* e *Soar Phoenix* são tratadas como a mesma peça.  
- Peças com design diferente e nomes distintos são consideradas únicas.  
  - Ex: *Roar Tyranno ≠ Soar Phoenix*  
- Variações de tipo com o mesmo nome (ex: Lightning L-Drago tipo “upper” e tipo “rapid-hit”) são consideradas a mesma peça.  
- ❌ Não é permitido trocar peças entre os Beys do deck durante uma partida.

---

### 📦 DeckBox — Informações Adicionais
- Obrigatória em partidas no formato **3-on-3**.  
- Deve possuir **compartimentos separados** para cada Beyblade.  
- A abertura de cada compartimento deve ser **individual**.  
- O material deve ser **opaco**, impedindo visualização do conteúdo.  
- A ordem dos combos deve ser definida **da esquerda para a direita**.  
- Recomenda-se adicionar **identificação numérica** em cada compartimento.

---

### 🚀 Lançador
- O lançador é o dispositivo utilizado para lançar o Bey na arena.  
- Qualquer acessório conectado ao lançador é considerado parte oficial dele e segue as mesmas regras.

---

### 🏟️ Estádio — Regras Oficiais OBA
- As batalhas acontecem dentro do estádio, composto por duas partes principais:  
  - **Tampa do Estádio**: área de lançamento (abertura circular).  
  - **Corpo do Estádio**: superfície onde os Beys batalham.

#### ⚔️ Zonas do Estádio
- O espaço interno é dividido em **três zonas** que influenciam a batalha:

🔵 **Zona de Batalha (Battle Zone)**  
- Área principal onde os Beys giram e se enfrentam.  

🕳️ **Zona Over (Over Zone)**  
- Dois bolsões localizados nas laterais frontais do estádio.  
- Um Bey que cai aqui pode ser considerado fora de jogo.  

🚨 **Zona Xtreme (Xtreme Zone)**  
- A grande abertura frontal central do estádio.  
- Beys que saem por aqui normalmente resultam em **pontos de vitória** para o oponente.

🔎 Um Bey é considerado dentro de uma zona assim que a **maior parte de sua estrutura** estiver dentro da respectiva área.

> **Obs:** Se um Bey sair por um local que **não seja Over ou Xtreme Zone**, o round é **anulado e repetido**.

---

## 🧩 Fases da Partida

### 🕐 Preliminares
- Cada participante deve preparar seus combos antecipadamente.  
- No formato 3-on-3, a ordem deve ser definida antes da batalha na presença do juiz.

### 🏁 Início da Partida
- A partida começa quando ambos os Bladers e o juiz estão presentes.  
- ❌ Não é permitido receber ajuda de terceiros.  
- ❌ Não é permitido sair do estádio sem autorização.  
- ❌ Não é permitido tocar no Beyblade sem autorização do juiz.

---

### 🌀 Posição de Lançamento
- Antes do primeiro set: sorteio define o lado (ex: cara ou coroa).  
- Nos sets seguintes: quem perdeu o anterior escolhe o lado.  

---

### 📣 Apresentação do Bey
- O juiz entrega os Beys e anuncia as combinações.  
- Após isso, os bladers podem:  
  - Girar o Ratchet ou Bit.  
  - Mudar modos de peças que permitem isso.  
- Devem **avisar o juiz e o oponente** antes de ajustar.  
- É **proibido tocar no Bey do oponente**.

---

### ⚔️ Batalha
- A batalha ocorre até que um Blader atinja a pontuação necessária.  
- No formato 3-on-3, o juiz apresenta os próximos combos na sequência definida.

---

### 🎮 Tipos de Partida
🔹 **1 contra 1 (1on1)**  
- Cada Blader seleciona um único Bey.  

🔸 **3 contra 3 (3on3)**  
- Cada Blader monta um deck com 3 Beys ordenados.  
- Pode possuir **um combo extra** para alternar entre batalhas.

---

### 🌀 Regras do Deck
- Após cada batalha, o juiz entrega o próximo Bey conforme a ordem.  
- Após o 3º Bey, se não houver vencedor:  
  - Os Bladers podem **reordenar o deck** antes da próxima rodada.  
- O deck deve permanecer **oculto** e **na mesma ordem** até o final da rodada.

---

## ⚔️ Regras da Batalha

### 🚀 Lançamento
- Verifique se o Bey está montado corretamente.  
- Lance seu Bey **a no máximo 20cm** do corpo do estádio.  
- Não obstrua o lançamento do oponente.  
- Não toque ou mova o estádio.  
- Após o lançamento, recue e observe.  

---

### ❌ Erros de Lançamento
Um erro ocorre quando o Blader:
- Puxa antes/depois do comando “shoot/rip”.  
- Lança de mais de 20cm.  
- Lança de fora da área designada.  
- Lança o Bey de cabeça para baixo ou de lado.  
- O Bey toca o estádio antes da área de lançamento.  

**Penalidade:**  
- A cada 2 erros, o oponente ganha **1 ponto**.  
- Se ambos errarem, nenhum ponto é dado.

---

### ⚔️ Início e Fim da Batalha
- Começa quando ambos os Beys tocam o chão.  
- Um Bey está fora de jogo quando:
  - Para de girar 🌀  
  - Se desmonta 💥  
  - Sai do estádio 🚫  

❗ Não toque no estádio até o juiz confirmar o resultado.

---

### 🏆 Pontuação por Finalizações
| Tipo de Finalização | Pontos | Condição |
|----------------------|--------|-----------|
| Xtreme Finish | **3 pts** | O Bey oponente entra na Xtreme Zone |
| Over Finish | **2 pts** | O Bey oponente entra na Over Zone |
| Burst Finish | **2 pts** | Oponente eclode |
| Spin Finish | **1 pt** | Oponente para de girar |

---

### 🔄 Batalhas Anuladas e Repetidas
- Empate 🤝  
- Erro de lançamento  
- Interferência  
- Quebra de peças  
- Obstrução  

Na repetição:
- Mesmo Beys e lançadores (exceto em caso de quebra).  
- Bits podem ser girados e peças reapertadas.

---

## ⚖️ Decisões do Juiz
- Dúvidas devem ser reportadas imediatamente.  
- Após o início da próxima batalha, resultados não mudam.  
- A decisão final é sempre do(s) juiz(es).  
- Recusar a decisão pode resultar em **desclassificação**.

---

## ⚙️ Regulamento de Equipamentos

### 🧱 Regras Gerais
- Apenas produtos oficiais **Takara Tomy** e **Hasbro**.  
- Gerações anteriores não são permitidas.  
- Estádios permitidos:
  - **Xtreme Stadium (Takara Tomy)**  
  - **Xtreme BeyStadium (Hasbro)**  
- Equipamentos trincados ou quebrados ❌  
- Reparos permitidos apenas se:
  - Fita por baixo.  
  - Superfície lisa.  
  - Sem reforço estrutural.

---

### 🌀 Regulamento de Beys
- Desgaste extremo é proibido.  
- Borracha pode desgastar, desde que funcional.  
- Peças com defeito de fabricação que afetam desempenho são proibidas.

---

### 🚀 Regulamento de Lançadores
- Winder Launchers aceitam qualquer tipo de winder (Winder, Long, Entry, Dragon).  
- ❌ Winders não podem ser modificados.  
- Pode decorar com tinta/adesivo, desde que discreto e sem alterar desempenho.  
- Imagens ofensivas são proibidas.

---

### 🧩 Acessórios
- Permitidos se **não atrapalharem o oponente** ou **alterarem desempenho**.

---

### 🚫 Peças Banidas
*(Lista será publicada separadamente conforme atualizações oficiais.)*

---

## ⚠️ Desclassificação
Você pode ser desclassificado se:
- Quebrar regras intencionalmente.  
- Usar equipamento irregular.  
- Lançar de forma perigosa.  
- Agir de forma desrespeitosa.  

**Consequências:**
- Perda do confronto e colocação.  
- Possível suspensão de eventos futuros.  
""")


with tabTwo: # ABA TABELA COMPLETA
    df["blader_id"] = df["blader_id"].astype(int).astype(str).str.zfill(3)

     # porcentagem
    df["duel_win_loss_percentage_fmt"] = (df["duel_win_loss_percentage"] * 100).round(2).astype(str) + "%"


    st.dataframe(
    df[["blader_id", "blader", "points", "matches", "wins", "losses", "win_loss_ratio", "duels", "duel_win", "duel_loss", "duel_win_loss_percentage_fmt"]]
    .rename(columns={
        "blader_id": "ID",
        "blader": "Nome",
        "points": "Pontos",
        "matches": "Partidas",
        "wins": "Vitórias",
        "losses": "Derrotas",
        "win_loss_ratio": "Taxa V/D",
        "duels":"Duelos",
        "duel_win":"Duelos: Vitórias",
        "duel_loss":"Duelos: Derrotas",
        "duel_win_loss_percentage_fmt":"Duelos: Porcentagem de Vitórias"
    }),
    use_container_width=True
)

with tabSix:  # ABA GERADOR BLADER TAG
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
            stats_font  = ImageFont.truetype("fonts/American Captain.ttf", 12)

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
            stats_y = pts_y + (bbox[3]-bbox[1]) + 30
            for line in stats:
                bbox = stats_font.getbbox(line)
                x = (tag_img.width - (bbox[2]-bbox[0])) // 2
                draw.text((x, stats_y), line, font=stats_font, fill="white")
                stats_y += (bbox[3]-bbox[1]) + 5

            # DUEL STATS
            duel_win = int(row.get("duel_win", 0))
            duel_loss = int(row.get("duel_loss", 0))
            duel_pct = float(row.get("duel_win_loss_percentage", 0)) * 100
            duel_stats = [
                f"Duelos: Vitorias: {duel_win}",
                f"Duelos: Derrotas: {duel_loss}",
                f"Duelos: % Vitorias: {duel_pct:.1f}%"
            ]
            for line in duel_stats:
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
