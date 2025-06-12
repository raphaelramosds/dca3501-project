from abc import ABC, abstractmethod
from services.dataframes import *

import streamlit as st
import pandas as pd
import plotly.express as px


class Plotter(ABC):
    dataframe: type[BaseDataFrame]

    def __init__(self, filters: dict = {}):
        self.filters: dict = filters
        self.df: pd.DataFrame = self.dataframe.mount()
        if filters:
            self.df = self.filter()

    def render(self):
        self.plot()

    # TODO: filtering should be BaseDataFrame responsibility
    @abstractmethod
    def filter(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def plot(self):
        pass


class AqiMapPlotter(Plotter):
    dataframe = AnnualAqiDataFrame

    def filter(self):
        df_filtered = self.df.copy()
        if 'year' in self.filters:
            df_filtered = df_filtered[df_filtered['Year'] == self.filters['year']]
        return df_filtered

    def plot(self):
        fig = px.scatter_mapbox(
            self.df,
            lat="Lat",
            lon="Lon",
            hover_name="City",
            hover_data={"AQI": True, "Lat": False, "Lon": False},
            size="AQI",
            color="AQI",
            # TODO: turn color_discrete_map continous and set here for following the color scheme
            color_continuous_scale="RdYlGn_r",
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

    def filter(self):
        df_filtered = self.df.copy()
        if 'year' in self.filters:
            df_filtered = df_filtered[df_filtered['Year'] == self.filters['year']]
        return df_filtered

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

    def filter(self):
        return super().filter()
    
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