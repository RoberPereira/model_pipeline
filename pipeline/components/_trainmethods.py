from ._pipemethods import (PipelineMethod, MethodResult)
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


class LoadEtl(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

    def execute(self, last_results: list) -> MethodResult:
        '''Load Etl'''
        logger.info(f"Loading etl. {self.params}")

        load_output = self.find_result(last_results, 'load').get('result').get_output()
        version = self.params.get('version')

        if load_output:
            path_name = f'{load_output.get("output_processed")}_v{version}'
        else:
            s_date = self.params.get('startdate')
            e_date = self.params.get('enddate')
            path_name = f'processed/{self.params.get("stock")}_{s_date}_{e_date}_v{version}'

        data = joblib.load(f'data/{path_name}')

        output = {'path_name': path_name}
        self.passthrough(self.params, output, 'succes', {'data': data})

        logger.info(f"Done loading etl. {path_name}")
        return self.mresult


class ComputeTarget(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

    def execute(self, last_results: list) -> MethodResult:
        '''Compute target.'''
        logger.info(f"Execute target computation. {self.params}")

        tdefiner = TargetDefiner(self.params)
        datasets = self.previews_restult(last_results).get_datasets()
        data = tdefiner.compute_target(datasets.get('data'))
        datasets['data'] = data

        output = {'target_columns': tdefiner.get_target_columns()}
        self.passthrough(self.params, output, 'succes', datasets)

        return self.mresult


class ComputeFeatures(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

    def execute(self, last_results: list) -> MethodResult:
        '''Compute features.'''
        logger.info(f"Execute features computation. {self.params}")

        self.passthrough(self.params, {}, 'succes',
                         self.previews_restult(last_results).get_datasets())

        return self.mresult


class DataSplitter(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

    def execute(self, last_results: list) -> MethodResult:
        ''' Compute data splitting '''

        logger.info(f'Execute Data Splitter. {self.params}')
        data = self.previews_restult(last_results).get_dataset()

        splitter = DataSplitterCustom(self.params, data)
        ds_train, ds_test = splitter.split_train_test(data)

        datasets = {'ds_train': ds_train,
                    'ds_test': ds_test,
                    'data': data}

        self.passthrough(self.params, {}, 'succes', datasets)

        return self.mresult


class ModelBuilder(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

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
                                           ).get('result').get_input_params()
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

        datasets = self.previews_restult(last_results).get_datasets()
        self.passthrough(self.params, {}, 'succes', datasets, pipeline)
        return self.mresult


class ModelTrainer(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

    def execute(self, last_results: list) -> MethodResult:
        logger.info(f'Execute Model train. {self.params}')

        ds_train = self.find_result(last_results, 'data_split'
                                    ).get('result').get_dataset('ds_train')
        ds_test = self.find_result(last_results, 'data_split'
                                   ).get('result').get_dataset('ds_test')
        target = self.find_result(last_results, 'compute_target'
                                  ).get('result').get_output().get('target_columns')
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

        output = {'model_metrics': model_metrics.to_dict()}
        datasets = self.previews_restult(last_results).get_datasets()
        self.passthrough(self.params, output, 'succes', datasets, pipeline)
        return self.mresult


class SaveModel(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)

    def execute(self, last_results: list) -> MethodResult:
        logger.info(f'Saving Model. {self.params}')

        pipeline = self.find_result(last_results, 'train'
                                    ).get('result').get_pipeline()
        model_metadata = self.find_result(last_results, 'build_model'
                                          ).get('result').get_input_params()

        version = self.version
        type = model_metadata.get('model').get('type')
        identifier = self.params.get('identifier')
        name = f'{type}_{identifier}_v{version}.dat'
        pickle.dump(pipeline, open(f'models/{name}', "wb"))

        output = {'model_name': name}
        datasets = self.previews_restult(last_results).get_datasets()
        self.passthrough(self.params, output, 'succes', datasets, pipeline)
        return self.mresult
