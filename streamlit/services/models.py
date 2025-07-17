from statsmodels.tsa.deterministic import DeterministicProcess
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class AqiForecasterModel():
    
    def __init__(self, time_series : pd.DataFrame) -> None:
        y = time_series.copy()

        dp = DeterministicProcess(
            index=y.index,
            order=3
        )

        X = dp.in_sample()

        model = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)
        model.fit(X, y)

        X_fore = dp.out_of_sample(steps=12)
        y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

        self.y = y
        self.y_fore = y_fore
        
    
    def get_y_fore(self):
        return self.y_fore

    def get_y_fore_one(self):
        return self.y_fore.iloc[0]
    
    def get_aqi_reference(self):
        return self.y.iloc[-1]['AQI']