from statsmodels.tsa.deterministic import DeterministicProcess
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class AqiForecasterModel:
    
    def __init__(self, time_series : pd.DataFrame) -> None:
        y = time_series.copy()

        dp = DeterministicProcess(
            index=y.index,
            order=3
        )

        X = dp.in_sample()

        model = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)
        self.__model = model.fit(X, y)

    def predict(self, num_steps : int = 1) -> float:
        X_fore = dp.out_of_sample(steps=num_steps)

        y_fore = pd.Series(self.__model.predict(X_fore), index=X_fore.index)

        return list(zip(X_fore, y_fore))