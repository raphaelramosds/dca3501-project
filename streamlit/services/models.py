from statsmodels.tsa.deterministic import DeterministicProcess
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class AqiForecasterModel:
    
    def __init__(self, time_series : pd.DataFrame) -> None:
        print(time_series)
        y = time_series.copy()

        dp = DeterministicProcess(
            index=y.index,
            order=3
        )

        X = dp.in_sample()

        model = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)
        model.fit(X, y)

        X_fore = dp.out_of_sample(steps=1)
        y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

        self.fore_month_aqi = list(zip(X_fore, y_fore))

    def get_aqi_fore(self):
        return self.fore_month_aqi[0][1]
    
    def get_month_fore(self):
        return self.fore_month_aqi[0][0]