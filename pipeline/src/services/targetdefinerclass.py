import pandas as pd


class TargetDefiner():

    def __init__(self, config) -> None:
        self.config = config

    def compute_target(self, ds: pd.DataFrame):
        targets_forecast_days = self.config.get('forecast_day')
        target_prefix = self.config.get('prefix')
        target_postfix = self.config.get('postfix')
        target_on_column = self.config.get('on_column')

        for t in targets_forecast_days:
            target_series = ds[target_on_column].shift(-t).to_frame().rename(
                columns={target_on_column: f'{target_prefix}{t}{target_postfix}'})

            ds = pd.concat([ds, target_series], axis=1)

        return ds

    def get_target_columns(self):
        prefix = self.config.get('prefix')
        postfix = self.config.get('postfix')
        targets_forecast_days = self.config.get('forecast_days')

        return [f'{prefix}{t}{postfix}' for t in targets_forecast_days]
