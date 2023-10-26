import pandas as pd


class DataSplitter():

    def __init__(self, config, ds: pd.DataFrame) -> None:
        self.config = config
        (self.__train_idx,
         self.__test_idx,
         self.__eval_idx,
         self.__forecast_idx) = self.__compute_training_idx(ds)

    def get_train_idx(self):
        return self.__train_idx

    def get_test_idx(self):
        return self.__test_idx

    def get_eval_idx(self):
        return self.__eval_idx

    def get_forecast_idx(self):
        return self.__forecast_idx

    def split_train_test(self, ds_data: pd.DataFrame):

        ds_train = ds_data.loc[self.__train_idx[0]: self.__train_idx[-1]]
        ds_test = ds_data.loc[self.__test_idx[0]: self.__test_idx[-1]]

        return ds_train, ds_test

    def split_datasets(self, ds_data: pd.DataFrame):

        ds_train = ds_data.loc[self.__train_idx[0]: self.__train_idx[-1]]
        ds_test = ds_data.loc[self.__test_idx[0]: self.__test_idx[-1]]
        ds_eval = ds_data.loc[self.__eval_idx[0]: self.__eval_idx[-2]]
        ds_forecast = ds_data.loc[self.__eval_idx[-1]:]

        return ds_train, ds_test, ds_eval, ds_forecast

    def __compute_training_idx(self, ds_data: pd.DataFrame):
        # 23 days Periods ( Aprox 1 month,  Buisiness Days only)
        day_periods = self.config.train.forecast_days

        # 1 Month for evaluation
        dt_eval_idx = pd.bdate_range(end=ds_data.index[-1],
                                     periods=day_periods, freq='B')

        # 3 Month for testing and prediction interval calculation
        dt_test_idx = pd.bdate_range(end=dt_eval_idx[0],
                                     periods=day_periods * 3,
                                     freq='B', inclusive='left')

        # Rest for Training , exluding first 23 days for feature computation
        dt_start_training_idx = pd.bdate_range(start=ds_data.index[0],
                                               periods=day_periods + 2,
                                               freq='B')[-1]

        dt_training_idx = pd.bdate_range(start=dt_start_training_idx,
                                         end=dt_test_idx[0],
                                         freq='B',
                                         inclusive='left')

        # 1 Month forecast
        dt_forecast_idx = pd.bdate_range(start=dt_eval_idx[-1],
                                         periods=day_periods, freq='B')

        return dt_training_idx, dt_test_idx, dt_eval_idx, dt_forecast_idx
