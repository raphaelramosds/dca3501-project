import streamlit as st
import plotly.express as px
import pandas as pd
import random

# Dados das cidades com valores aleatórios de AQI
cities = [
    {"city": "Patna", "lat": 25.5941, "lon": 85.1376},
    {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"city": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"city": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"city": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"city": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"city": "Amritsar", "lat": 31.6340, "lon": 74.8723},
]

# Gerar AQI aleatório entre 150 e 700
for city in cities:
    city["AQI"] = random.randint(150, 700)

# Converter para DataFrame
df = pd.DataFrame(cities)

# Criar o mapa com AQI como tamanho e cor
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="city",
    hover_data={"AQI": True, "lat": False, "lon": False},
    size="AQI",                # Tamanho da bolinha
    color="AQI",               # Cor com base no AQI
    color_continuous_scale="RdYlGn_r",  # Escala de cores invertida (verde bom → vermelho ruim)
    zoom=4,
    center={"lat": 22.9734, "lon": 78.6569},
    height=600
)

# Estilo do mapa
fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    title="Índice de Qualidade do Ar (AQI) nas Cidades Indianas"
)

# Renderização no Streamlit
def render_india_map():
    st.subheader("🗺️ AQI nas Cidades da Índia")
    st.plotly_chart(fig, use_container_width=True)
