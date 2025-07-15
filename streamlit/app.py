import streamlit as st

from services.dataframes import AnnualAqiDataFrame
from services.plotters import *

title = "Qualidade do Ar na Índia"

st.set_page_config(
    page_title=title,
    layout="wide",
    page_icon="public/in.svg",
)


st.title("{} 🌤️".format(title))

tabs = st.tabs(
    [
        "📊 IQA Anual",
        "📈 IQA x Matéria Particulada (PM)",
        "ℹ️ Previsão de IQA",
    ]
)

# Tab IQA Anual
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        cities = st.multiselect(
            "Escolha uma Cidade",
            options=AnnualAqiDataFrame.mount()["City"].unique(),
            default=[
                "Ahmedabad",
                "Amritsar",
                "Chennai",
                "Delhi",
                "Jaipur",
                "Lucknow",
                "Mumbai",
                "Patna",
            ],
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
        AqiSunburstPlotter({"year": year, "city": cities}).render()


@st.cache_data
def render_series():
    SeriesAqiParticlesPlotter({}).render()
    
def render_gauge():
    AqiGaugePlotter({}).render()


# Tab IQA x Matéria Particulada
with tabs[1]:
    render_series()
    

with tabs[2]: 
    st.markdown(
        "Para prever o IQA, é necessário escolher uma cidade e um modelo de previsão."
    )
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox(
            "Escolha uma Cidade",
            options=AnnualAqiDataFrame.mount()["City"].unique(),
        )

    if city:
        st.write(f"Previsão do IQA para a cidade {city} usando o modelo RandomForest.")
        # Aqui você pode adicionar a lógica para previsão com base no modelo escolhido.
        
        render_gauge();
