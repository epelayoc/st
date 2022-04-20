import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image

# colnames= {c:c for c in list(df)}

# Title
image = Image.open('KDT-JU.png')
st.image(image)
st.title("Partner search")

# Select country
countries = ['ES', 'FR', 'DE']
ct = {'ES': 'Spain', 'DE': 'Germany', 'FR':'France'}
country = st.selectbox('Select country',countries)
st.write(f'You selected: {country}-{ct[country]}')

# SQL queries
conn = sqlite3.connect('mockDB.db')
df_grants = pd.read_sql(f"SELECT year, grants FROM grants WHERE country = '{country}' ", conn)
df_grants = df_grants.set_index('year')
df_participants = pd.read_sql(f"SELECT * FROM participants WHERE country = '{country}' ", conn)
df_coordinators = pd.read_sql(f"SELECT * FROM coordinators WHERE country = '{country}' ", conn)
conn.close()

# grants
st.subheader(f'Yearly EC contribution in {ct[country]} (€)')
st.bar_chart(df_grants)

# participants
st.subheader(f'Participants in {ct[country]}')
st.dataframe(df_participants)
csv_p = df_participants.to_csv().encode('utf-8')
st.download_button(
     label="Download participants data as CSV",
     data=csv_p,
     file_name=f'{country}_participants.csv',
     mime='text/csv',
 )

# coordinators
st.subheader(f'Project cooordinators in {ct[country]}')
st.dataframe(df_coordinators)
csv_c = df_coordinators.to_csv().encode('utf-8')
st.download_button(
     label="Download coordinators data as CSV",
     data=csv_c,
     file_name=f'{country}_coordinators.csv',
     mime='text/csv',
 )
