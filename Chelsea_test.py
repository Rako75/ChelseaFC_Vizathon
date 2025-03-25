import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les fichiers CSV
@st.cache_data
def load_data():
    gps_data = pd.read_csv("CFC GPS Data.csv", encoding='ISO-8859-1')
    physical_data = pd.read_csv("CFC Physical Capability Data_.csv")
    return gps_data, physical_data

# Charger les données
gps_data, physical_data = load_data()

# Titre de l'application
st.title("CFC Performance Dashboard")

# Sidebar pour filtrage
st.sidebar.header("Filtres")
selected_date = st.sidebar.selectbox("Sélectionner une date", gps_data['date'].unique())
selected_season = st.sidebar.selectbox("Sélectionner une saison", gps_data['season'].unique())

# Filtrer les données
gps_filtered = gps_data[(gps_data['date'] == selected_date) & (gps_data['season'] == selected_season)]
physical_filtered = physical_data[physical_data['season'] == selected_season]

# Section GPS Data
st.subheader("📍 Données GPS")
fig1 = px.line(gps_filtered, x='date', y=['distance', 'peak_speed'], title="Distance & Vitesse Maximale")
st.plotly_chart(fig1)

# Section Physical Capability
st.subheader("💪 Capacité Physique")
fig2 = px.bar(physical_filtered, x='MOVEMENTS', y='BenchmarkPct', color='QUALITY', title="Performance Physique")
st.plotly_chart(fig2)

# Résumé
st.subheader("Résumé des Performances")
st.write("GPS Data:")
st.dataframe(gps_filtered)
st.write("Physical Capability Data:")
st.dataframe(physical_filtered)

st.success("Dashboard interactif prêt !")
