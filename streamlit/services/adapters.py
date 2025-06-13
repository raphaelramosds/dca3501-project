from services.dataframes import BaseDataFrame
import pandas as pd

class DataFrameAdapter:
    def __init__(self, dataframe_cls: BaseDataFrame, filters: dict = None):
        self.dataframe_cls = dataframe_cls
        self.filters = filters or {}
        self.df = self.dataframe_cls.mount()

    def filter(self) -> pd.DataFrame:
        return self.dataframe_cls.filter(self.df, self.filters)