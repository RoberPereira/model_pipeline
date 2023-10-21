from . import train_config
import pandas as pd

__feature_columns = []


def compute_target_feature(ds_data: pd.DataFrame):

    config = train_config.get('target')
    targets_forecast_days = config.get('forecast_days')
    target_prefix = config.get('prefix')
    target_postfix = config.get('postfix')
    target_on_column = config.get('on_column')

    for t in targets_forecast_days:
        target_series = ds_data[target_on_column].shift(-t).to_frame().rename(
            columns={target_on_column: f'{target_prefix}{t}{target_postfix}'})

        ds_data = pd.concat([ds_data, target_series], axis=1)

    return ds_data


def compute_lag_features(ds_data: pd.DataFrame):

    config = train_config.get('features')
    features_on_columns = config.get('on_columns')
    day_windows = config.get('day_windows')

    for col in features_on_columns:
        for day_period in day_windows:

            series = ds_data[col].shift(day_period).to_frame().rename(
                columns={col: f'{col}_{day_period}d'})
            ds_data = pd.concat([ds_data, series], axis=1)
            __feature_columns.extend(series.columns.tolist())

            series = ds_data[col].diff(day_period).to_frame().rename(
                columns={col: f'{col}_diff_{day_period}d'})
            ds_data = pd.concat([ds_data, series], axis=1)
            __feature_columns.extend(series.columns.tolist())

            series = ds_data[col].rolling(day_period).mean().to_frame().rename(
                columns={col: f'{col}_mean_{day_period}d'})
            ds_data = pd.concat([ds_data, series], axis=1)
            __feature_columns.extend(series.columns.tolist())

            series = ds_data[col].rolling(
                day_period + 1).std().to_frame().rename(
                    columns={col: f'{col}_std_{day_period}d'})
            ds_data = pd.concat([ds_data, series], axis=1)
            __feature_columns.extend(series.columns.tolist())

    ds_data = pd.concat([ds_data, pd.DataFrame(ds_data.index.dayofweek
                                               .rename('day_of_week'),
                                               index=ds_data.index)], axis=1)

    ds_data = pd.concat([ds_data, pd.DataFrame(ds_data.index.dayofyear
                                               .rename('day_of_year'),
                                               index=ds_data.index)], axis=1)

    ds_data = pd.concat([ds_data, pd.DataFrame(ds_data.index.month
                                               .rename('month'),
                                               index=ds_data.index)], axis=1)

    __feature_columns.extend(['day_of_week', 'day_of_year', 'month'])

    return ds_data


def get_target_columns():
    config = train_config.get('target')
    prefix = config.get('prefix')
    postfix = config.get('postfix')
    targets_forecast_days = config.get('forecast_days')

    return [f'{prefix}{t}{postfix}' for t in targets_forecast_days]


def get_features_columns():
    return __feature_columns
