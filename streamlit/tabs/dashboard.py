import sys
sys.path.append('../')

import streamlit as st
import components.india_map as india_map
import components.sunburst_aqi as sunburst_aqi

def render_dashboard():
    st.subheader("Dashboard")
    st.write("Aqui vai o conteúdo da dashboard!")
    col1, col2 = st.columns(2)
    with col1:
        india_map.render_india_map()
    with col2:
        st.write("Coluna 2: Gráficos e análises")
        sunburst_aqi.render_sunburst_aqi()
        
        
    