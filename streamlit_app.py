import streamlit as st
from datetime import date
import requests
import io
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from streamlit_gsheets import GSheetsConnection

# PAGE CONFIG
st.set_page_config(page_title="Ranking - OBA", page_icon=":shark:")
tabOne, tabTwo, tabThree, tabFour, tabFive, tabSix = st.tabs(["🏆 Top 10", "📋 Ranking Completo", "🗓️ Próximo Evento", "✅ Regras Oficiais", "🦈 Regras Especiais", "🐞 Gerar Blader Tag"])

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

    st.markdown("""
    ## 🏆 Vencendo uma Partida

    Em torneios, os jogos de Beyblade são disputados em **partidas**, compostas por **batalhas**, **pontos** e **sets**:

    - **Batalha:** Quando dois Beys se enfrentam e um vencedor é definido. O resultado concede pontos.
    - **Pontos:** São concedidos com base na forma como a batalha foi vencida (ver seção de *tipos de finalizações*).
    - **Set:** Vencido quando um blader atinge o número de pontos exigido.

    **Pontuação necessária para vencer um set:**
    - Fase inicial: **4 pontos** (padrão)
    - Fase final: **7 pontos** (padrão)

    **Formato da partida:**
    - **Melhor de 1 (Bo1):** vence quem ganhar 1 set
    - **Melhor de 3 (Bo3):** vence quem ganhar 2 sets

    ---

    ## 🧩 Fases da Partida

    ### Início da Partida
    A partida começa assim que ambos os bladers e o juiz estiverem presentes no estádio designado.

    - A partir desse momento, **não é permitido receber ajuda ou conselhos de terceiros**.
    - Exceções podem ser feitas a critério do juiz (ex.: bladers com necessidades especiais).
    - Não é permitido **sair do estádio** sem autorização do juiz.

    ---

    ### 🌀 Posição de Lançamento
    - Um dos bladers escolhe o lado de lançamento (esquerdo ou direito).
    - Antes do primeiro set, essa escolha é definida por sorteio justo (ex.: par ou ímpar, cara ou coroa).
    - Nos sets seguintes, **quem perdeu o set anterior escolhe o lado de lançamento**.
    - O outro blader deve assumir o lado restante.

    ---

    ### 🧱 Escolha do Bey
    - Bladers escolhem seus Beys **em segredo** (ex.: virados de costas para o estádio).
    - A escolha deve ser feita em **até 1 minuto**. Após esse tempo, o juiz pode exigir decisão imediata.
    - É proibido tentar **obter informações sobre o Bey do oponente**.
    - Após a escolha, os Beys são **entregues ao juiz para inspeção** (inclusive desmontagem, se necessário).
    - A escolha do Bey ou deck é **definitiva para a partida**.
    - Entre os sets, os Beys **não são reinspecionados**, mas a ordem do deck pode ser alterada.

    ---

    ### 📣 Apresentação do Bey
    - Cada blader deve **mostrar o topo e a base do seu Bey ao oponente**, com todas as peças visíveis.
    - Após essa apresentação, os bladers podem **ajustar seus Beys**:
    - Alterar a posição de peças (ex.: girar o ratchet ou bit)
    - Mudar o modo de peças que possuem essa funcionalidade
    - Mesmo que o ajuste exija desmontagem
    - O blader deve **avisar o oponente e o juiz** antes de ajustar o Bey.
    - Após o ajuste, o Bey deve ser apresentado novamente.
    - **É proibido tocar no Bey do oponente.**

    ---

    ### ⚔️ Batalha
    - A batalha ocorre conforme as regras até que um blader atinja a pontuação necessária para vencer o set.
    - Se o Bey for trocado entre batalhas (ex.: formato 3 contra 3), o processo de **apresentação do Bey deve ser repetido**.

    ---

    ### ✅ Resultado da Partida
    - Quando um blader vence o número de sets necessário, o juiz confirma e encerra a partida.
    - Caso nenhum tenha vencido ainda, a partida continua com o próximo set, reiniciando a escolha de posição.

    """)

    st.markdown("---")

    st.markdown("""
    ## 🎮 Tipos de Partida

    ---

    ### 🔹 1 contra 1 (1on1)
    - Cada blader seleciona **um único Bey**.
    - A partida continua até que seja determinado um vencedor.

    ---

    ### 🔸 3 contra 3 (3on3)
    - Cada blader monta um **deck com 3 Beys**, ordenados da **esquerda para a direita** como:
    - 1º Bey
    - 2º Bey
    - 3º Bey

    #### Regras:
    - Após cada batalha, o blader deve trocar para o próximo Bey do deck.
    - Após utilizar o 3º Bey, se não houver vencedor:
    - Os bladers podem **reordenar seu deck** antes de voltar ao 1º Bey.
    - O deck deve ser armazenado de forma que:
    - **Oculte seu conteúdo**;
    - **Mantenha a ordem dos Beys** (uso de *deck case* oficial é recomendado).
    - A ordem dos Beys **só pode ser alterada após a batalha com o 3º Bey**.

    ---

    ### 🟣 Deck WBO
    - Cada blader usa um **deck com até 3 Beys**.
    - O **perdedor de cada batalha** decide entre:

    - **🔁 Replay**: ambos repetem a batalha com o **mesmo Bey e lançador** (sem ajustes).
    - **🔄 Switch**: ambos podem trocar de Bey, com o **vencedor apresentando primeiro**.

    #### Fases:
    1. Na primeira apresentação, os dois jogadores mostram **todo o deck**.
    2. Em seguida, cada blader escolhe **em segredo** qual Bey usará na primeira batalha.
    3. Após cada batalha:
    - Se replay for escolhido, a batalha é repetida sem mudar os pontos anteriores.
    - Se switch for escolhido:
        - O vencedor apresenta seu novo Bey primeiro.
        - O perdedor então escolhe e apresenta o seu.

    ---

    ### 🔺 Pick 3 Choose 1 (P3C1)
    - Cada blader monta um **deck com até 3 Beys**.
    - Durante a fase de seleção:
    - Os dois jogadores mostram **todo o deck** para o oponente e o juiz.
    - Após isso, voltam à seleção e escolhem **em segredo** um único Bey para usar no set.
    - O Bey escolhido é então apresentado, e será usado até que haja um vencedor.
    """)

    st.markdown("---") # DIVISOR

    st.markdown("## 🧨 Regras da Batalha")

    st.markdown("### 🚀 Lançamento")
    st.markdown("""
    - Certifique-se de que seu Bey está corretamente montado, apertando o catraco e pressionando o bit.  
    - Prenda seu Bey no lançador e segure-o acima ou dentro da área de lançamento (figura 3).  
    - Mantenha o bit do seu Bey voltado para baixo enquanto estiver preso ao lançador. Não incline o lançador para que o bit fique de lado ou para cima.  
    - O juiz anunciará “prontos, preparar” para informar que a contagem regressiva para o lançamento está prestes a começar. Se você não estiver pronto, avise o juiz imediatamente.  
    - Durante a contagem, o juiz dirá: “três, dois, um, atire!” ou “três, dois, um, let it rip!”  
    - Comece a puxar a corda/lança assim que a palavra “atire”/“rip” for dita.  
    - Lance seu Bey a no máximo 20cm do corpo do estádio (figura 4).  
    - Não obstrua o lançamento do oponente.  
    - Não tente atingir o Bey do oponente antes que ele toque o corpo do estádio.  
    - Não corra, pule ou faça lançamentos de forma perigosa.  
    - Não toque ou mova o estádio ou sua base durante o lançamento.  
    - Após o lançamento, recue imediatamente e observe a batalha. Não se incline sobre o estádio.
    """)

    st.markdown("### ❌ Erros de Lançamento")
    st.markdown("""
    Um blader comete erro de lançamento quando:

    - Começa a puxar a corda antes ou depois da palavra “atire”/“rip”  
    - Lança de mais de 20cm de distância do estádio  
    - Lança de fora da área designada de lançamento  
    - Lança seu Bey para fora do estádio  
    - Lança seu Bey de cabeça para baixo ou de lado  
    - O Bey toca a cobertura do estádio antes de passar pela área de lançamento  
    - Toca o estádio com o corpo ou o lançador (exceto a corda)

    **Resultado**: o duelo é anulado.  
    **Penalidade**: a cada 2 erros sem pontuação, o oponente ganha 1 ponto.  

    Se ambos cometerem erro no mesmo lançamento, nenhum ponto é concedido.
    """)

    st.markdown("### 🔁 Solicitação de Relançamento")
    st.markdown("""
    Você pode pedir um relançamento se:

    - O lançamento do oponente obstruiu o seu  
    - Foi atingido ou impedido por alguém ou algo  
    - Seu lançamento foi fraco devido a problema técnico com o lançador  

    **Procedimento**:

    - Diga “relançar” imediatamente após lançar.  
    - Se aprovado, a batalha é anulada.  
    - Se o problema foi técnico, use um lançador diferente pelo restante da partida.  
    - Se não tiver outro, pode emprestar de outro blader.  
    - Só é permitido um relançamento técnico por batalha.  
    - O juiz pode testar seu lançador.  
    - Apenas o blader afetado pode solicitar; o juiz ou oponente não podem sugerir.
    """)

    st.markdown("### ⚔️ Início e Fim da Batalha")
    st.markdown("""
    - A batalha começa quando ambos os Beys tocam o estádio.  
    - Um Bey está **fora de jogo** quando:

    - Para de girar (velocidade de rotação = 0)  
    - Se desmonta (explosão)  
    - Sai do estádio e não pode voltar  

    A batalha termina quando:

    - Só um Bey está girando, ou  
    - Todos os Beys estão fora de jogo  

    ⚠️ **Não toque no estádio ou Bey até o juiz confirmar o resultado**. Caso contrário, você pode perder a rodada.
    """)

    st.markdown("### 🏆 Pontuação por Finalizações")
    st.markdown("""
    | Tipo de Finalização | Pontos | Condições |
    |---------------------|--------|-----------|
    | **Xtreme Finish**   | 3 pts  | Oponente entra na zona Xtreme e fica fora de jogo |
    | **Over Finish**     | 2 pts  | Oponente entra na zona Over e fica fora de jogo |
    | **Burst Finish**    | 2 pts  | Oponente se desmonta |
    | **Spin Finish**     | 1 pt   | Oponente para de girar |

    - Uma finalização é **iniciada** quando o oponente sai ou fica fora de jogo.  
    - A vitória só é confirmada quando a finalização é **pontuada**.  
    - Se o oponente voltar à zona de batalha, a finalização é **anulada**.  
    - Se ambos pontuarem, vence quem **iniciou** primeiro.  
    - Se iniciarem ao mesmo tempo e pontuarem, a batalha é **empate**.  
    - Se ninguém pontuar, também é empate.
    """)

    st.markdown("### 🔄 Batalhas Anuladas e Repetidas")
    st.markdown("""
    A batalha é **anulada** se:

    - Terminar em empate  
    - Ocorreu erro de lançamento  
    - Os Beys se tocam antes de ambos tocarem o estádio  
    - Um Bey explode antes de tocar o estádio  
    - Um Bey sai sem passar pelas zonas Xtreme/Over  
    - O juiz determinar que houve obstrução  
    - Foi solicitado e aprovado relançamento  
    - Alguma peça do Bey quebrou  
    - O estádio quebrou ou parte dele se soltou  
    - Qualquer outra interferência relevante  

    Na repetição:

    - Usam-se os mesmos Beys e lançadores, exceto em caso de quebra  
    - Bits podem ser girados e catracos apertados, mas não é permitido desmontar o Bey  
    - Se não puder substituir a peça quebrada, ambos retornam à fase de seleção, mantendo a pontuação
    """)

    st.markdown("### ⚖️ Decisões do Juiz")
    st.markdown("""
    - Qualquer dúvida deve ser reportada ao juiz imediatamente.  
    - Após o início da próxima batalha, o resultado anterior não será alterado.  
    - O juiz pode revisar vídeos da batalha se quiser.  
    - Em alguns torneios, há juiz principal para apelação.  
    - A decisão final é sempre do(s) juiz(es).  
    - **Não aceitar a decisão do juiz pode levar à desclassificação.**
    """)

    st.write("Regras adaptadas e traduzidas da página oficial de regras da WBO (World Beyblade Organization)")
    st.markdown('<a href="https://worldbeyblade.org/Thread-Beyblade-X-Rules" target="_blank">🔗 Acessar regras oficias WBO</a>', unsafe_allow_html=True)

with tabFive:
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
