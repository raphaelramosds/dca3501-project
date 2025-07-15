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
            options=AnnualAqiDataFrame.list_cities(),
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
            options=AnnualAqiDataFrame.list_years(),
        )

    col1, col2 = st.columns(2)
    with col1:
        AqiMapPlotter({"year": year, "city": cities}).render()
    with col2:
        AqiSunburstPlotter({"year": year, "city": cities}).render()


# Tab IQA x Matéria Particulada
with tabs[1]:
    @st.cache_data
    def render_series():
        SeriesAqiParticlesPlotter({}).render()
    render_series()
    

# Tab Previsão de IQA
with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        O indicador ao lado mostra a previsão do IQA para o mês seguinte ao último registro de qualidade do ar nesta cidade.
                    
        Além disso, também mostramos a variação prevista para o mês em questão.
                    
        **Observação:** Uma variação negativa significa que o IQA abaixou, implicando uma melhoria na qualidade do ar.
        """)
        city = st.selectbox(
            "Escolha a cidade",
            options=AqiTimeSeriesDataFrame.list_cities(),
        )
    with col2:
        @st.cache_data
        def render_gauge(filters : dict = {}):
            AqiGaugePlotter(filters).render()
        render_gauge({"city": city} if city else {});
