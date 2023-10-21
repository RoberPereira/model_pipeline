from etl import config
import pandas as pd


class FeatureEngineering():

    __feature_columns = []

    def __init__(self) -> None:
        pass

    def compute_target_feature(self, ds_data: pd.DataFrame):

        target = config.target
        targets_forecast_days = target.forecast_days
        target_prefix = target.prefix
        target_postfix = target.postfix
        target_on_column = target.on_column

        for t in targets_forecast_days:
            target_series = ds_data[target_on_column].shift(-t).to_frame().rename(
                columns={target_on_column: f'{target_prefix}{t}{target_postfix}'})

            ds_data = pd.concat([ds_data, target_series], axis=1)

        return ds_data

    def compute_lag_features(self, ds_data: pd.DataFrame):

        features = config.features
        features_on_columns = features.on_columns
        day_windows = features.day_windows

        for col in features_on_columns:
            for day_period in day_windows:

                series = ds_data[col].shift(day_period).to_frame().rename(
                    columns={col: f'{col}_{day_period}d'})
                ds_data = pd.concat([ds_data, series], axis=1)
                self.__feature_columns.extend(series.columns.tolist())

                series = ds_data[col].diff(day_period).to_frame().rename(
                    columns={col: f'{col}_diff_{day_period}d'})
                ds_data = pd.concat([ds_data, series], axis=1)
                self.__feature_columns.extend(series.columns.tolist())

                series = ds_data[col].rolling(day_period).mean().to_frame().rename(
                    columns={col: f'{col}_mean_{day_period}d'})
                ds_data = pd.concat([ds_data, series], axis=1)
                self.__feature_columns.extend(series.columns.tolist())

                series = ds_data[col].rolling(
                    day_period + 1).std().to_frame().rename(
                        columns={col: f'{col}_std_{day_period}d'})
                ds_data = pd.concat([ds_data, series], axis=1)
                self.__feature_columns.extend(series.columns.tolist())

        ds_data = pd.concat([ds_data, pd.DataFrame(ds_data.index.dayofweek
                                                   .rename('day_of_week'),
                                                   index=ds_data.index)],
                            axis=1)

        ds_data = pd.concat([ds_data, pd.DataFrame(ds_data.index.dayofyear
                                                   .rename('day_of_year'),
                                                   index=ds_data.index)],
                            axis=1)

        ds_data = pd.concat([ds_data, pd.DataFrame(ds_data.index.month
                                                   .rename('month'),
                                                   index=ds_data.index)],
                            axis=1)

        self.__feature_columns.extend(['day_of_week', 'day_of_year', 'month'])

        return ds_data

    def get_target_columns(self):
        target = config.target
        prefix = target.prefix
        postfix = target.postfix
        targets_forecast_days = target.forecast_days

        return [f'{prefix}{t}{postfix}' for t in targets_forecast_days]

    def get_features_columns(self):
        return self.__feature_columns
