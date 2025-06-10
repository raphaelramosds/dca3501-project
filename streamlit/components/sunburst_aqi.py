import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Cidades
cities = [
    "Patna", "Mumbai", "Lucknow", "Jaipur",
    "Delhi", "Chennai", "Ahmedabad", "Amritsar"
]

# Função para classificar o AQI
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy SG"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# Gerar DataFrame com valores aleatórios
data = []
for city in cities:
    aqi = random.randint(30, 500)
    category = classify_aqi(aqi)
    data.append({"city": city, "AQI": aqi, "category": category})

df = pd.DataFrame(data)

# Criar gráfico sunburst
fig = px.sunburst(
    df,
    path=["category", "city"],
    values="AQI",
    color="category",
    color_discrete_map={
        "Good": "green",
        "Moderate": "yellow",
        "Unhealthy SG": "orange",
        "Unhealthy": "red",
        "Very Unhealthy": "purple",
        "Hazardous": "maroon"
    },
    title="Distribuição de AQI por Categoria e Cidade"
)

# Mostrar no Streamlit
def render_sunburst_aqi():
    st.subheader("🌞 Gráfico Sunburst de AQI por Cidade")
    st.plotly_chart(fig, use_container_width=True)
