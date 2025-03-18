import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Charger les données CSV
gps_data = pd.read_csv("CFC GPS Data.csv")
physical_capability_data = pd.read_csv("CFC Physical Capability Data_.csv")
recovery_status_data = pd.read_csv("CFC Recovery status Data.csv")
priority_areas_data = pd.read_csv("CFC Individual Priority Areas.csv")

# Conversion de la colonne 'date' en datetime
gps_data['date'] = pd.to_datetime(gps_data['date'])
physical_capability_data['date'] = pd.to_datetime(physical_capability_data['date'])
recovery_status_data['date'] = pd.to_datetime(recovery_status_data['date'])

# Titre de l'application
st.title("Suivi de la Performance Physique et Récupération du Joueur")

# Ajouter une barre latérale pour la navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choisir une vue", ["GPS Data", "Physical Capability", "Recovery Status", "Individual Priority Areas"])

# ----------------------------------------------
# GPS Data Visualization
if app_mode == "GPS Data":
    st.header("Suivi GPS du Joueur")

    # Calcul de la distance totale parcourue par jour
    distance_total = gps_data.groupby('date')['distance'].sum()

    # Afficher le graphique de la distance parcourue
    st.subheader("Distance totale parcourue par le joueur")
    plt.figure(figsize=(10, 6))
    plt.plot(distance_total.index, distance_total.values)
    plt.title("Distance totale parcourue par le joueur")
    plt.xlabel("Date")
    plt.ylabel("Distance (m)")
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)

# ----------------------------------------------
# Physical Capability Visualization
elif app_mode == "Physical Capability":
    st.header("Suivi de la Capacité Physique du Joueur")

    # Sélectionner les colonnes pertinentes pour la visualisation
    sprint_data = physical_capability_data[physical_capability_data['MOVEMENT'] == 'Sprint']
    sprint_max_velocity = sprint_data[['date', 'QUALITY', 'EXPRESSION', 'BenchmarkPct']]

    # Visualiser les données de performance
    st.subheader("Performance Sprint du Joueur")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sprint_max_velocity['date'], sprint_max_velocity['BenchmarkPct'], label="Sprint Max Velocity")
    ax.set_title("Performance Sprint du joueur")
    ax.set_xlabel("Date")
    ax.set_ylabel("Benchmark %")
    ax.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

# ----------------------------------------------
# Recovery Status Visualization
elif app_mode == "Recovery Status":
    st.header("Suivi de la Récupération du Joueur")

    # Visualiser les données de sommeil
    sleep_data = recovery_status_data[['date', 'Sleep_composite']]

    st.subheader("Qualité du Sommeil du Joueur")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sleep_data['date'], sleep_data['Sleep_composite'], label="Score Composite du Sommeil")
    ax.set_title("Qualité du Sommeil du joueur")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score Composite")
    ax.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

# ----------------------------------------------
# Individual Priority Areas
elif app_mode == "Individual Priority Areas":
    st.header("Priorités Individuelles du Joueur")

    # Afficher le tableau des priorités
    st.subheader("Priorités actuelles")
    st.dataframe(priority_areas_data)

    # Sélectionner une priorité
    priority = st.selectbox("Choisir une priorité", priority_areas_data['Priority'])
    selected_priority = priority_areas_data[priority_areas_data['Priority'] == priority]
    st.write(f"Priorité sélectionnée : {selected_priority[['Category', 'Area', 'Target', 'Performance Type', 'Tracking']].to_string(index=False)}")
