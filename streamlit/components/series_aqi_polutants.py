import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Lista atualizada de cidades
cities = [
    "Patna", "Mumbai", "Lucknow", "Jaipur",
    "Delhi", "Chennai", "Ahmedabad", "Amritsar"
]

# Geração de dados simulados realistas para cada mês entre 2015 e 2020
def gerar_dados_simulados(cities):
    datas = pd.date_range(start='2015-01-01', end='2020-12-31', freq='MS')  # mensal
    dados = []

    for data in datas:
        mes_str = data.strftime('%Y-%m')
        for cidade in cities:
            # Geração de dados diferenciados por cidade
            base_pm25 = 90 + hash(cidade) % 60
            base_pm10 = 140 + hash(cidade[::-1]) % 70

            pm25 = np.random.normal(loc=base_pm25, scale=15)
            pm10 = np.random.normal(loc=base_pm10, scale=20)
            aqi = (pm25 * 0.5 + pm10 * 0.5) + np.random.normal(scale=8)

            dados.append({
                'cidade': cidade,
                'mes': mes_str,
                'pm25': max(pm25, 0),
                'pm10': max(pm10, 0),
                'aqi': max(aqi, 0)
            })

    return pd.DataFrame(dados)

# Gerar os dados
df = gerar_dados_simulados(cities)

# Calcular limites dos eixos com padding
padding_x = (df['pm25'].max() - df['pm25'].min()) * 0.05
padding_y = (df['pm10'].max() - df['pm10'].min()) * 0.05

range_x = [df['pm25'].min() - padding_x, df['pm25'].max() + padding_x]
range_y = [df['pm10'].min() - padding_y, df['pm10'].max() + padding_y]

# Criar o gráfico com Plotly Express
fig = px.scatter(
    df,
    x="pm25",
    y="pm10",
    animation_frame="mes",
    animation_group="cidade",
    size="aqi",
    color="cidade",
    hover_name="cidade",
    size_max=60,
    range_x=range_x,
    range_y=range_y,
    labels={'pm25': 'PM2.5 (µg/m³)', 'pm10': 'PM10 (µg/m³)', 'aqi': 'AQI médio'},
    title="Correlação mensal de PM2.5, PM10 e AQI por cidade (2015–2020)"
)

fig.update_layout(
    xaxis_title="Concentração média de PM2.5",
    yaxis_title="Concentração média de PM10",
    margin=dict(l=40, r=40, t=60, b=40),
    height=700
)

# Função para renderizar no Streamlit
def render_series_polutants():
    st.title("Correlação entre PM2.5, PM10 e AQI nas cidades indianas (2015–2020)")
    st.markdown("Cada ponto representa uma cidade em um mês. O tamanho indica o AQI médio.")
    st.plotly_chart(fig, use_container_width=True)

# Para execução direta
if __name__ == "__main__":
    render_series_polutants()
