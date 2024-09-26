import streamlit as st
import pandas as pd
import altair as alt

# Titre de l'application
st.title('Calculateur de Yield Management')

# Entrée utilisateur pour les variables
revenu_maximum = st.number_input("Revenu maximum (en euros)", value=1000)
taux_occupation_cible = st.slider("Taux d'occupation cible (en %)", 0.0, 1.0, 0.85)
taux_occupation_actuel = st.slider("Taux d'occupation actuel (en %)", 0.0, 1.0, 0.75)
elasticite_demande = st.number_input("Élasticité de la demande", value=1.5)

# Fonction pour calculer le prix idéal
def calculer_prix_ideal(revenu_maximum, taux_occupation_cible, taux_occupation_actuel, elasticite_demande):
    prix_ideal = (revenu_maximum * taux_occupation_cible) / (
        1 + elasticite_demande * (taux_occupation_cible - taux_occupation_actuel)
    )
    return prix_ideal

# Calculer le prix idéal en fonction des entrées utilisateur
prix = calculer_prix_ideal(revenu_maximum, taux_occupation_cible, taux_occupation_actuel, elasticite_demande)

# Afficher le résultat
st.write(f"Le prix idéal est : {prix:.2f} euros")

# Créer un DataFrame pour afficher les résultats
data = pd.DataFrame({
    'Taux occupation': [taux_occupation_cible, taux_occupation_actuel],  # Renommé sans apostrophe
    'Prix idéal': [prix, prix * 0.9]  # Exemple de variation de prix
})

# Afficher les données sous forme de tableau
st.write(data)

# Créer un graphique avec Altair
chart = alt.Chart(data).mark_line().encode(
    x='Taux occupation',  # Utilise le nom sans apostrophe
    y='Prix idéal'
)

# Afficher le graphique dans Streamlit
st.altair_chart(chart, use_container_width=True)
