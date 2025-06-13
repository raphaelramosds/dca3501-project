import streamlit as st

from pathlib import Path
from abc import ABC, abstractmethod

import pandas as pd

parent_dir = Path(__file__).resolve().parent.parent

class BaseDataFrame(ABC):
    path = None

    @classmethod
    def mount(cls) -> pd.DataFrame:
        if cls.path is None:
            raise NotImplementedError("Subclass should define `path` attribute.")
        return pd.read_csv(cls.path)

    @classmethod
    @abstractmethod
    def filter(cls, df: pd.DataFrame, filters: dict) -> pd.DataFrame:
        pass

class AnnualAqiDataFrame(BaseDataFrame):
    path = "{}/data/dashboard_annual_aqi.csv".format(parent_dir)

    @classmethod
    def filter(cls, df: pd.DataFrame, filters: dict) -> pd.DataFrame:
        mask = pd.Series(True, index=df.index)

        if 'city' in filters:
            cities = filters['city']
            if isinstance(cities, list):
                mask &= df['City'].isin(cities)
            else:
                mask &= df['City'] == cities

        if 'year' in filters:
            mask &= df['Year'] == filters['year']

        return df[mask]


class MonthlyAqiParticlesDataFrame(BaseDataFrame):
    path = "{}/data/dashboard_month_aqi_pm10_pm25.csv".format(parent_dir)
