from abc import ABC, abstractmethod
from services.dataframes import *

import streamlit as st
import pandas as pd
import plotly.express as px

from services.adapters import DataFrameAdapter


class Plotter(ABC):
    dataframe: type[BaseDataFrame]  # Should be set by subclass

    def __init__(self, filters: dict = {}):
        self.filters: dict = filters

        # Use adapter to mount and filter data
        self.adapter = DataFrameAdapter(self.dataframe, self.filters)
        self.df: pd.DataFrame = self.adapter.filter()

    def render(self):
        self.plot()

    @abstractmethod
    def plot(self):
        pass



class AqiMapPlotter(Plotter):
    dataframe = AnnualAqiDataFrame

    def plot(self):
        # Define a color scale for AQI 
        color_scale = [
            (0.0, "green"),       # Good
            (0.2, "yellow"),      # Moderate
            (0.4, "orange"),      # Poor
            (0.6, "pink"),        # Unhealthy
            (0.8, "purple"),      # Severe
            (1.0, "maroon"),      # Hazardous
        ]
        fig = px.scatter_mapbox(
            self.df,
            lat="Lat",
            lon="Lon",
            hover_name="City",
            hover_data={"AQI": True, "Lat": False, "Lon": False},
            size="AQI",
            color="AQI",
            # TODO: turn color_discrete_map continous and set here for following the color scheme
            color_continuous_scale=color_scale,
            range_color=[0, 300],
            zoom=4,
            center={"lat": 22.9734, "lon": 78.6569},
            height=600,
        )
        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            title="Índice de Qualidade do Ar (AQI) nas Cidades Indianas",
        )
        st.plotly_chart(fig, use_container_width=True)


class AqiSunburstPlotter(Plotter):
    dataframe = AnnualAqiDataFrame

    def plot(self):
        fig = px.sunburst(
            self.df,
            path=["AQI_Category", "City"],
            values="AQI",
            color="AQI_Category",
            color_discrete_map={
                "Good": "green",
                "Moderate": "yellow",
                "Poor": "orange",
                "Unhealthy": "pink",
                "Severe": "purple",
                "Hazardous": "maroon",
            },
            title="Distribuição de AQI por Categoria e Cidade",
        )

        fig.update_layout(
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)

class SeriesAqiParticlesPlotter(Plotter):
    dataframe = MonthlyAqiParticlesDataFrame
    
    def plot(self):

        padding_x = (self.df['PM2.5'].max() - self.df['PM2.5'].min()) * 0.05
        padding_y = (self.df['PM10'].max() - self.df['PM10'].min()) * 0.05

        range_x = [self.df['PM2.5'].min() - padding_x, self.df['PM2.5'].max() + padding_x]
        range_y = [self.df['PM10'].min() - padding_y, self.df['PM10'].max() + padding_y]

        fig = px.scatter(
            self.df,
            x="PM2.5",
            y="PM10",
            animation_frame="YearMonth",
            animation_group="City",
            size="AQI",
            color="City",
            hover_name="City",
            size_max=60,
            range_x=range_x,
            range_y=range_y,
            labels={'PM2.5': 'PM2.5 (µg/m³)', 'PM10': 'PM10 (µg/m³)', 'AQI': 'AQI médio'},
            title="Correlação mensal de PM2.5, PM10 e AQI por cidade (2015–2020)"
        )

        fig.update_layout(
            xaxis_title="Concentração média de PM2.5",
            yaxis_title="Concentração média de PM10",
            margin=dict(l=40, r=40, t=60, b=40),
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)