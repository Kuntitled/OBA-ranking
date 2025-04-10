import streamlit as st
from datetime import date
import pandas as pd
from streamlit_gsheets import GSheetsConnection

gSheetsConnection = st.connection("gsheets", type=GSheetsConnection)
df = gSheetsConnection.read(worksheet="Ranking Oficial")
df = df.dropna(how="all")

#st.dataframe(df)

st.set_page_config(page_title="Ranking - OBA", 
                   page_icon=":shark:"
                   )

today = str(date.today())

st.title("Organização de Beyblade do Amazonas")
st.write(today)
st.title("RANKING ATUAL")

# Get the first 3 rows using a for loop
first_three = []

for _, row in df.head(3).iterrows():  # .head(3) gets the first 3 rows
    first_three.append(row.to_dict())

# Convert back to DataFrame (optional)
first_three_df = pd.DataFrame(first_three)

# Show it in Streamlit
st.table(first_three_df)

#for row in df.itertuples()[:3]:
#    st.write(f"{row.blader} tem {row.points} e está em {row.placement}")

#for row in df.intertuples():
#    mainTable.append(row)

st.write(mainTable)