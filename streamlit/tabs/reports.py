import streamlit as st
import components.series_aqi_polutants as series_aqi_polutants

def render_reports():
    series_aqi_polutants.render_series_polutants()
