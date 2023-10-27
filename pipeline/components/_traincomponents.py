from ._mthdcomponents import (ComponentMethod, MethodResult)
from src.services.targetdefinerclass import TargetDefiner
from src.services.splitterclass import DataSplitterCustom
from src.services.aggregatorclass import FeatureAggregator
from src.model_functions import compute_evaluation_metrics
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import pandas as pd
import joblib
import pickle
import logging
import warnings

warnings.filterwarnings("ignore", "is_categorical_dtype")
logger = logging.getLogger('Logger')


class LoadEtl(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'load_etl')

    def execute(self, last_results: list) -> MethodResult:
        '''Load Etl'''
        logger.info(f"Loading etl. {self.params}")

        version = self.params.get('version')
        s_date = self.params.get('startdate')
        e_date = self.params.get('enddate')
        path_name = f'processed/{self.params.get("stock")}_{s_date}_{e_date}_v{version}'

        data = joblib.load(f'data/{path_name}')

        self.mresult.set_dataset(data)
        self.params['path_name'] = path_name
        self.mresult.set_metadata(self.params)

        logger.info(f"Done loading etl. {path_name}")
        return self.mresult


class ComputeTarget(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'compute_target')

    def execute(self, last_results: list) -> MethodResult:
        '''Compute target.'''
        logger.info(f"Execute target computation. {self.params}")

        tdefiner = TargetDefiner(self.params)
        last_result = last_results[-1].get('result')
        data = tdefiner.compute_target(last_result.get_dataset())
        target_columns = tdefiner.get_target_columns()
        self.mresult.set_dataset(data)
        self.params['target_columns'] = target_columns
        self.mresult.set_metadata(self.params)
        return self.mresult


class ComputeFeatures(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'compute_features')

    def execute(self, last_results: list) -> MethodResult:
        '''Compute features.'''
        logger.info(f"Execute features computation. {self.params}")

        self.mresult.set_dataset(last_results[-1].get('result').get_dataset())
        self.mresult.set_metadata(self.params)
        return self.mresult


class DataSplitter(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'data_split')

    def execute(self, last_results: list) -> MethodResult:
        ''' Compute data splitting '''

        logger.info(f'Execute Data Splitter. {self.params}')
        data = last_results[-1].get('result').get_dataset()

        splitter = DataSplitterCustom(self.params, data)
        ds_train, ds_test = splitter.split_train_test(data)

        self.mresult.set_dataset(data)
        self.mresult.set_dataset(ds_train, 'ds_train')
        self.mresult.set_dataset(ds_test, 'ds_test')
        self.mresult.set_metadata(self.params)
        return self.mresult


class ModelBuilder(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'build_model')

    def execute(self, last_results: list) -> MethodResult:
        logger.info(f'Building Model. {self.params}')

        model = xgb.XGBRegressor(
            n_estimators=27,
            max_depth=4,
            min_child_weight=1,
            eta=0.1,
            reg_lambda=0,
            objective='reg:squarederror',
            random_state=42)

        # this coupling between steps is do to merging feat. computation and training step
        features_params = self.find_result(last_results, 'compute_features'
                                           ).get('result').get_metadata()
        on_columns = features_params.get('on_columns')
        windows = features_params.get('day_windows')

        ct = ColumnTransformer([("selector", "passthrough", on_columns)],
                               verbose_feature_names_out=False,
                               remainder="drop").set_output(transform='pandas')

        pipeline = Pipeline([
            ("selector", ct),
            ('aggregator', FeatureAggregator(on_columns, windows)),
            ('scaler', StandardScaler()),
            ('model', model)
        ])

        self.mresult.set_pipeline(pipeline)
        self.mresult.set_dataset(last_results[-1].get('result').get_dataset())
        self.mresult.set_metadata(self.params)
        return self.mresult


class ModelTrainer(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'train')

    def execute(self, last_results: list) -> MethodResult:
        logger.info(f'Execute Model train. {self.params}')

        ds_train = self.find_result(last_results, 'data_split'
                                    ).get('result').get_dataset('ds_train')
        ds_test = self.find_result(last_results, 'data_split'
                                   ).get('result').get_dataset('ds_test')
        target = self.find_result(last_results, 'compute_target'
                                  ).get('result').get_metadata().get('target_columns')
        y_train = ds_train[target]
        y_test = ds_test[target]

        X_train_c = pd.concat([ds_train, ds_test], axis=0)
        y_train_c = pd.concat((y_train, y_test), axis=0)

        pipeline = self.find_result(last_results, 'build_model'
                                    ).get('result').get_pipeline()
        pipeline.fit(X_train_c, y_train_c, model__verbose=10)

        y_pred = pipeline.predict(X_train_c)
        model_metrics = compute_evaluation_metrics(y_train_c,
                                                   y_pred,
                                                   self.params.get('identifier'))

        self.params['model_metrics'] = model_metrics
        self.mresult.set_pipeline(pipeline)
        self.mresult.set_dataset(last_results[-1].get('result').get_dataset())
        self.mresult.set_metadata(self.params)
        return self.mresult


class SaveModel(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'save_model')

    def execute(self, last_results: list) -> MethodResult:
        logger.info(f'Saving Model. {self.params}')

        pipeline = self.find_result(last_results, 'train'
                                    ).get('result').get_pipeline()
        model_metadata = self.find_result(last_results, 'build_model'
                                          ).get('result').get_metadata()

        version = self.version
        type = model_metadata.get('model').get('type')
        identifier = self.params.get('identifier')
        name = f'{type}_{identifier}_v{version}.dat'
        pickle.dump(pipeline, open(f'models/{name}', "wb"))

        self.mresult.set_metadata(self.params)
        return self.mresult
