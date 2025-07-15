from pathlib import Path
from abc import ABC, abstractmethod

import pandas as pd

data_dir = Path(__file__).resolve().parent.parent / "data"

class BaseDataFrame(ABC):
    path = None

    @classmethod
    def mount(cls) -> pd.DataFrame:
        if cls.path is None:
            raise NotImplementedError("Subclass should define `path` attribute.")
        return pd.read_csv(cls.path)

    @classmethod
    @abstractmethod
    def filter(cls, filters: dict) -> pd.DataFrame:
        return cls.mount()


class AnnualAqiDataFrame(BaseDataFrame):
    path = data_dir / "dashboard_annual_aqi.csv"

    @classmethod
    def filter(cls, filters: dict) -> pd.DataFrame:
        df = cls.mount()
        
        mask = pd.Series(True, index=df.index)

        if "city" in filters:
            cities = filters["city"]
            if isinstance(cities, list):
                mask &= df["City"].isin(cities)
            else:
                mask &= df["City"] == cities

        if "year" in filters:
            mask &= df["Year"] == filters["year"]

        return df[mask]


class MonthlyAqiParticlesDataFrame(BaseDataFrame):
    path = data_dir / "dashboard_month_aqi_pm10_pm25.csv"


class AqiTimeSeriesDataFrame(BaseDataFrame):
    path = data_dir / "dashboard_aqi_time_series.csv"

    @classmethod
    def mount(cls) -> pd.DataFrame:
        return pd.read_csv(cls.path, index_col=['Date', 'City'])
    
    @classmethod
    def filter(cls, filters: dict) -> pd.DataFrame:
        df = cls.mount()
        
        mask = pd.Series(True, index=df.index)

        if "city" in filters:
            city = filters["city"]
            mask &= df["City"] == city

        return df[mask]