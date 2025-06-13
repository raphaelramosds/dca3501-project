import streamlit as st

from services.dataframes import AnnualAqiDataFrame
from services.plotters import *

st.set_page_config(page_title="India Weather Dashboard", layout="wide", page_icon="https://hatscripts.github.io/circle-flags/flags/in.svg")


st.title("India Weather Dashboard Analysis 🌤️")

tabs = st.tabs(
    [
        "📊 Cities AQI",
        "📈 Weather Polutants",
    ]
)


@st.cache_data
def render_series():
    SeriesAqiParticlesPlotter({}).render()


with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:    
        cities = st.multiselect(
            "Escolha uma Cidade",
            options=AnnualAqiDataFrame.mount()["City"].unique(),
            default=['Ahmedabad','Amritsar', 'Chennai', 'Delhi', 'Jaipur', 'Lucknow', 'Mumbai','Patna'],
            key="city",
        )
    with col2:
        year = st.selectbox(
            "Escolha um Ano",
            options=AnnualAqiDataFrame.mount()["Year"].unique(),
        )
        
    col1, col2 = st.columns(2)
    with col1:
        AqiMapPlotter({"year": year, "city": cities}).render()
    with col2:
        AqiSunburstPlotter({"year": year,  "city": cities}).render()

with tabs[1]:
    render_series()
    # SeriesAqiParticlesPlotter({}).render()

# with tabs[2]:
#     render_settings()
