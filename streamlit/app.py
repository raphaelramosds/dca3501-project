import streamlit as st

# from tabs.dashboard import render_dashboard
# from tabs.reports import render_reports
# from tabs.settings import render_settings

from services.dataframes import AnnualAqiDataFrame
from services.plotters import *

st.set_page_config(page_title="India Weather Dashboard", layout="wide")

st.title("India Weather Dashboard Analysis 🌤️")

tabs = st.tabs(
    [
        "📊 Cities AQI",
        "📈 Weather Polutants",
        # "⚙️ Configuration"
    ]
)


@st.cache_data
def render_series():
    SeriesAqiParticlesPlotter({}).render()


with tabs[0]:
    # TODO: transform into dropdown
    year = st.select_slider(
        "Escolha um Ano",
        options=AnnualAqiDataFrame.mount()["Year"].unique(),
    )
    col1, col2 = st.columns(2)
    with col1:
        AqiMapPlotter({"year": year}).render()
    with col2:
        AqiSunburstPlotter({"year": year}).render()

with tabs[1]:
    render_series()
    # SeriesAqiParticlesPlotter({}).render()

# with tabs[2]:
#     render_settings()
