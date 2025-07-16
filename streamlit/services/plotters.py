from abc import ABC, abstractmethod
from datetime import datetime
from services.dataframes import *
from services.models import AqiForecasterModel

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


class Plotter(ABC):
    dataframe: type[BaseDataFrame]

    def __init__(self, filters: dict = {}):
        self.df = self.dataframe.filter(filters)

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
            (0.0, "green"),  # Good
            (0.2, "yellow"),  # Moderate
            (0.4, "orange"),  # Poor
            (0.6, "pink"),  # Unhealthy
            (0.8, "purple"),  # Severe
            (1.0, "maroon"),  # Hazardous
        ]
        fig = px.scatter_mapbox(
            self.df,
            lat="Lat",
            lon="Lon",
            hover_name="City",
            hover_data={"AQI": True, "Lat": False, "Lon": False},
            size="AQI",
            color="AQI",
            color_continuous_scale=color_scale,
            range_color=[0, 300],
            zoom=4,
            center={"lat": 22.9734, "lon": 78.6569},
            height=600,
        )
        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            title="Índice de Qualidade do Ar (IQA) médio anual",
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
            # title="Distribuição de AQI por Categoria e Cidade",
        )

        fig.update_layout(
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)

class AqiGaugePlotter(Plotter):
    dataframe = AqiTimeSeriesDataFrame

    def plot(self):
        model = AqiForecasterModel(self.df)
        aqi_value = model.get_aqi_fore()
        aqi_reference = model.get_aqi_reference()

        # Definir a cor da barra principal baseada no valor do AQI
        if aqi_value <= 50:
            bar_color = "#4CAF50"  # Verde vibrante
        elif aqi_value <= 100:
            bar_color = "#FFEB3B"  # Amarelo vibrante
        elif aqi_value <= 200:
            bar_color = "#FF9800"  # Laranja vibrante
        elif aqi_value <= 300:
            bar_color = "#F44336"  # Vermelho vibrante
        elif aqi_value <= 400:
            bar_color = "#9C27B0"  # Roxo vibrante
        else:
            bar_color = "#A24857"  # Marrom vibrante

        # Definir as faixas de cores padrão
        steps = [
            {"range": [0, 50], "color": "#4CAF50"},     # Verde
            {"range": [51, 100], "color": "#FFEB3B"},   # Amarelo
            {"range": [101, 200], "color": "#FF9800"},  # Laranja
            {"range": [201, 300], "color": "#F44336"},  # Vermelho
            {"range": [301, 400], "color": "#9C27B0"}, # Roxo
            {"range": [401, 500], "color": "#A24857"}  # Vinho
        ]

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=aqi_value,
                delta={"reference": aqi_reference},
                title={"text": f"Previsão"},
                gauge={
                    "axis": {"range": [None, 500]},
                    "bar": {"color": bar_color, "thickness": 0},
                    "steps": steps,
                    "threshold": {
                        "line": {"color": "black", "width": 5},
                        "thickness": 0.85,
                        "value": aqi_value
                    }
                },
            )
        )

        fig.update_layout(
            height=400,
            width=600,
            margin=dict(t=50, b=0, l=0, r=0),
            font={"color": "white", "family": "Arial"}
        )

        st.plotly_chart(fig, use_container_width=True)
    
class AqiTimeSeriesPlotter(Plotter):
    dataframe = AqiTimeSeriesDataFrame

    def plot(self):
        
        # Calcular a média móvel do AQI
        aqi_trend = self.df.rolling(
            window=12,
            center=True,
            min_periods=6,
        ).mean()

        # Converter índices Period para Datetime64
        months = self.df.index.get_level_values(level=0)
        month_axis = [datetime.strptime(month, "%Y-%m").strftime("%Y-%m-%d") for month in months]
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=month_axis,
            y=self.df['AQI'],
            mode='lines',
            name='AQI',
            line=dict(color='lightgray'),
        ))

        fig.add_trace(go.Scatter(
            x=month_axis,
            y=aqi_trend['AQI'],
            mode='lines',
            name='Média Móvel',
            line=dict(color='blue', width=3),
        ))

        fig.update_layout(
            title='Evolução do Índice de Qualidade do Ar',
            xaxis_title='Data',
            yaxis_title='AQI',
            legend=dict(x=0.01, y=0.99),
            template='plotly_white',
        )

        st.plotly_chart(fig, use_container_width=True)
        
class SeriesAqiParticlesPlotter(Plotter):
    dataframe = MonthlyAqiParticlesDataFrame

    def plot(self):

        padding_x = (self.df["PM2.5"].max() - self.df["PM2.5"].min()) * 0.05
        padding_y = (self.df["PM10"].max() - self.df["PM10"].min()) * 0.05

        range_x = [
            self.df["PM2.5"].min() - padding_x,
            self.df["PM2.5"].max() + padding_x,
        ]
        range_y = [self.df["PM10"].min() - padding_y, self.df["PM10"].max() + padding_y]

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
            labels={
                "PM2.5": "PM2.5 (µg/m³)",
                "PM10": "PM10 (µg/m³)",
                "AQI": "AQI médio",
            },
            title="Evolução mensal entre IQA e Matéria Particulada (PM) por cidade",
        )

        fig.update_layout(
            xaxis_title="Concentração média de PM2.5",
            yaxis_title="Concentração média de PM10",
            margin=dict(l=40, r=40, t=60, b=40),
            height=700,
        )

        st.plotly_chart(fig, use_container_width=True)
