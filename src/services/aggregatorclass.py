from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class FeatureAggregator(BaseEstimator, TransformerMixin):
    agg_features_ = []

    def __init__(self, on_columns: list, windows: list) -> None:
        self.agg_features_ = []
        self.on_columns = on_columns
        self.windows = windows

    def fit(self, X, y=None):
        current_columns = set(X.columns.tolist())
        X = self.__aggregate_features(X)
        self.agg_features_ = [x for x in X.columns.tolist()
                              if x not in current_columns]
        return self

    def transform(self, X, y=None):
        return self.__aggregate_features(X)[self.agg_features_]

    def __aggregate_features(self, X):
        for col in self.on_columns:
            for day_period in self.windows:

                series = X[col].shift(day_period).to_frame().rename(
                    columns={col: f'{col}_{day_period}d'})
                X = pd.concat([X, series], axis=1)

                series = X[col].diff(day_period).to_frame().rename(
                    columns={col: f'{col}_diff_{day_period}d'})
                X = pd.concat([X, series], axis=1)

                series = X[col].rolling(day_period).mean().to_frame().rename(
                    columns={col: f'{col}_mean_{day_period}d'})
                X = pd.concat([X, series], axis=1)

                series = X[col].rolling(
                    day_period + 1).std().to_frame().rename(
                        columns={col: f'{col}_std_{day_period}d'})
                X = pd.concat([X, series], axis=1)

        X = pd.concat([X, pd.DataFrame(X.index.dayofweek
                                       .rename('day_of_week'),
                                       index=X.index)],
                      axis=1)

        X = pd.concat([X, pd.DataFrame(X.index.dayofyear
                                       .rename('day_of_year'),
                                       index=X.index)],
                      axis=1)

        X = pd.concat([X, pd.DataFrame(X.index.month
                                       .rename('month'),
                                       index=X.index)],
                      axis=1)
        return X
