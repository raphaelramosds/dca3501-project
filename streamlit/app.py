import streamlit as st
from tabs.dashboard import render_dashboard
from tabs.reports import render_reports
from tabs.settings import render_settings

st.set_page_config(page_title="India Weather Dashboard", layout="wide")

st.title("India Weather Dashboard Analysis 🌤️")

tabs = st.tabs(["📊 Cities AQI", "📈 Weather Polutants", "⚙️ Configuration"])

with tabs[0]:
    render_dashboard()

with tabs[1]:
    render_reports()

with tabs[2]:
    render_settings()
