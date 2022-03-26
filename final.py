import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image


database = 'ecsel_database.db'

selects = {
'country': 
''' SELECT Acronym FROM countries WHERE Country = "{}" ''',
 
'grants': 
''' SELECT SUM(o.ecContribution) AS grants 
    FROM organizations o JOIN projects p ON o.projectID==p.projectID
    WHERE o.country = '{}'
    GROUP BY p.year ''',
    
'participants':  
''' SELECT shortName, name, activityType, organizationURL, COUNT(ecContribution) n_projects, SUM(ecContribution) grants 
    FROM organizations 
    WHERE country =  '{}' 
    GROUP BY name ORDER BY SUM(ecContribution) DESC ''',
    
'coordinators': 
''' SELECT o.shortName, o.name, p.acronym, p.keywords 
    FROM organizations o JOIN projects p ON o.projectID = p.projectID 
    WHERE o.country = '{}' AND o.role ='coordinator' '''
}

# Title
image = Image.open('KDT-JU.png')

st.image(image)
st.title("Partner search tool")

# Select country
conn = sqlite3.connect(database)
ct = st.selectbox('Select country',
     ['Spain', 'France', 'Germany'])
country = pd.read_sql(selects['country'].format(ct), conn)
country = country.Acronym.item()
st.write(f'You selected: {country}-{ct}')

# Other selects
dfs = {}
for key,sel in selects.items():
    dfs[key]=pd.read_sql(sel.format(country), conn)  
conn.close()

# grants
st.subheader(f'Yearly EC contribution in {ct} (€)')
st.bar_chart(dfs['grants'])

# participants
st.subheader(f'Participants in {ct}')
st.dataframe(dfs['participants'])
csv_p = dfs['participants'].to_csv().encode('utf-8')
st.download_button(
     label="Download participants data as CSV",
     data=csv_p,
     file_name=f'{country}_participants.csv',
     mime='text/csv',
 )

# coordinators
st.subheader(f'Project cooordinators in {ct}')
st.dataframe(dfs['coordinators'])
csv_c = dfs['coordinators'].to_csv().encode('utf-8')
st.download_button(
     label="Download coordinators data as CSV",
     data=csv_c,
     file_name=f'{country}_coordinators.csv',
     mime='text/csv',
 )