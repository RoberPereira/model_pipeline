import pandas as pd
from sklearn.preprocessing import StandardScaler


class Transformer():

    def __init__(self, features) -> None:
        self.__features = features

    def scale_data(self, ds: pd.DataFrame):
        scaler = StandardScaler()
        return scaler.fit_transform(ds[self.__features])
