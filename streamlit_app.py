import streamlit as st
import numpy as np
import plotly.express as px

def calculate_dynamic_price(base_price, season, anticipation, demand, difficulty, special_trip):
    # Coefficients de variation selon les facteurs
    season_factor = {'basse': 0.8, 'moyenne': 1.0, 'haute': 1.3}
    anticipation_factor = {'derniere_minute': 1.2, 'standard': 1.0, 'anticipee': 0.9}
    demand_factor = {'faible': 0.8, 'moyenne': 1.0, 'forte': 1.2}
    difficulty_factor = 1 + (difficulty - 1) * 0.1  # Augmente le prix en fonction de la difficulté
    special_trip_factor = 1.2 if special_trip else 1.0  # Augmente le prix si séjour spécial
    
    # Calcul du prix ajusté
    adjusted_price = (base_price * season_factor[season] * 
                      anticipation_factor[anticipation] * 
                      demand_factor[demand] * 
                      difficulty_factor * 
                      special_trip_factor)
    return round(adjusted_price, 2)

# Interface Streamlit
st.title("Outil de Yield Management pour Travel Planneuse")

# Entrées utilisateur
base_price = st.number_input("Prix de base du séjour (€)", min_value=100, max_value=5000, value=1500)
season = st.selectbox("Saisonnalité", ['basse', 'moyenne', 'haute'])
anticipation = st.selectbox("Anticipation de réservation", ['derniere_minute', 'standard', 'anticipee'])
demand = st.selectbox("Demande actuelle", ['faible', 'moyenne', 'forte'])
difficulty = st.slider("Difficulté du pays (1 = facile, 5 = difficile)", min_value=1, max_value=5, value=1)
special_trip = st.checkbox("Séjour spécial (voyage de noces, EVG/EVJF...)")

# Calcul du prix ajusté
adjusted_price = calculate_dynamic_price(base_price, season, anticipation, demand, difficulty, special_trip)
st.write(f"### Prix ajusté : {adjusted_price} €")

# Graphique interactif de simulation
seasons = ['basse', 'moyenne', 'haute']
prices = [calculate_dynamic_price(base_price, s, anticipation, demand, difficulty, special_trip) for s in seasons]
fig = px.bar(x=seasons, y=prices, labels={'x': "Saisonnalité", 'y': "Prix ajusté (€)"},
             title="Variation du prix selon la saison", color=prices, color_continuous_scale="viridis")
st.plotly_chart(fig)

# Graphique de répartition des facteurs d'influence
factors = ['Saison', 'Anticipation', 'Demande', 'Difficulté', 'Séjour spécial']
factor_values = [
    base_price * season_factor[season] - base_price,
    base_price * anticipation_factor[anticipation] - base_price,
    base_price * demand_factor[demand] - base_price,
    base_price * (difficulty_factor - 1),
    base_price * (0.2 if special_trip else 0)
]
fig2 = px.pie(values=factor_values, names=factors, title="Impact des facteurs sur le prix ajusté")
st.plotly_chart(fig2)
