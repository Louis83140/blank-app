import streamlit as st
import pandas as pd
import altair as alt

# En-tête et sous-titre avec emojis
st.title("💼 Calculateur de Yield Management")
st.subheader("Optimisez vos prix en fonction de la demande 📊")
st.markdown("Cette application vous permet de **calculer le prix idéal** pour vos services en fonction de la demande, du taux d'occupation, et de l'élasticité de la demande.")

# Barre latérale pour les paramètres
st.sidebar.header("🔧 Paramètres")
revenu_maximum = st.sidebar.number_input("💶 Revenu maximum (en euros)", value=1000)
elasticite_demande = st.sidebar.number_input("📈 Élasticité de la demande", value=1.5)

# Colonnes pour les sliders
col1, col2 = st.columns(2)
with col1:
    taux_occupation_cible = st.slider("Taux d'occupation cible", 0.0, 1.0, 0.85)

with col2:
    taux_occupation_actuel = st.slider("Taux d'occupation actuel", 0.0, 1.0, 0.75)

# Calcul du prix idéal
def calculer_prix_ideal(revenu_maximum, taux_occupation_cible, taux_occupation_actuel, elasticite_demande):
    prix_ideal = (revenu_maximum * taux_occupation_cible) / (
        1 + elasticite_demande * (taux_occupation_cible - taux_occupation_actuel)
    )
    return prix_ideal

prix = calculer_prix_ideal(revenu_maximum, taux_occupation_cible, taux_occupation_actuel, elasticite_demande)
st.write(f"### 💰 Le prix idéal est : **{prix:.2f} euros**")

# DataFrame et graphique
data = pd.DataFrame({
    "Taux occupation": [taux_occupation_cible, taux_occupation_actuel],
    "Prix idéal": [prix, prix * 0.9]
})

st.write("### 🔍 Résultats détaillés")
st.write(data)

# Graphique Altair avec personnalisation
chart = alt.Chart(data).mark_line(color='orange', strokeWidth=3).encode(
    x='Taux occupation',
    y='Prix idéal'
).properties(
    width=600,
    height=400,
    title="📊 Évolution du prix en fonction du taux d'occupation"
)
st.altair_chart(chart, use_container_width=True)

# Section déroulante pour les explications
with st.expander("ℹ️ Comment fonctionne cette application ?"):
    st.write("""
        Cette application utilise des formules économiques pour calculer le **prix idéal** selon différents paramètres.
        Vous pouvez ajuster les variables dans les champs ci-dessus pour voir les résultats en temps réel.
    """)
