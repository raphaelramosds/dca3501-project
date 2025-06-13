from services.dataframes import BaseDataFrame
import pandas as pd

class DataFrameAdapter:
    def __init__(self, df_cls: BaseDataFrame, filters: dict = None):
        self.df_cls = df_cls
        self.filters = filters or {}
        self.df = self.df_cls.mount()

    def filter(self) -> pd.DataFrame:
        return self.df_cls.filter(self.df, self.filters)