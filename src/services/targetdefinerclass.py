from etl import config
import pandas as pd


class TargetDefiner():

    def __init__(self) -> None:
        pass

    def compute_target(self, ds_data: pd.DataFrame):

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

    def get_target_columns(self):
        target = config.target
        prefix = target.prefix
        postfix = target.postfix
        targets_forecast_days = target.forecast_days

        return [f'{prefix}{t}{postfix}' for t in targets_forecast_days]
