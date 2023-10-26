from src.model_functions import compute_evaluation_metrics
from src.services.splitterclass import DataSplitter
from src.services.aggregatorclass import FeatureAggregator

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import pickle
import joblib
import json

import warnings
warnings.filterwarnings("ignore", "is_categorical_dtype")


class Train():

    def __init__(self, config) -> None:
        self.config = config

    def load_data(self, params):

        print(f'Fetching {params.get("stock")} stock data')
        pass

    def compute_features(self, params):

        print(f'compute_features ')
        pass

    def get_model(self, params):

        print(f'get_model')
        pass

    def train(self, params):

        print(f'train on columns ')
        pass

    def run(self, parmas):
        print('Start training...')

        ds_data = joblib.load(f'data/processed/{parmas.output_processed}')

        splitter = DataSplitter(ds_data)
        ds_train, ds_test = splitter.split_train_test(ds_data)

        target = 'target' # etl_metadata.target
        y_train = ds_train[target]
        y_test = ds_test[target]

        X_train_c = pd.concat([ds_train, ds_test], axis=0)
        y_train_c = pd.concat((y_train, y_test), axis=0)

        print('Training model...')
        pipeline = self.get_model()
        pipeline.fit(X_train_c, y_train_c, model__verbose=10)

        print('Saving model...')
        model_name = self.__save_model(pipeline)

        y_pred = pipeline.predict(X_train_c)
        model_metrics = compute_evaluation_metrics(y_train_c,
                                                   y_pred, model_name)

        print('Saving metadata...')
        model_features = pipeline['aggregator'].agg_features_
        self.__save_metadata(model_name, model_metrics.to_json(),
                             model_features)

        print('Training model DONE SUCCESSFULLY')

    def __save_metadata(self, model_name, model_metrics, model_features):
        self.metadata = {
            'etl_version': self.config.etl_version,
            'train_version': self.config.version,
            'output_model': model_name,
            'metrics': model_metrics,
            # 'etl_metadata': etl_metadata_serialized,
            'features': model_features
        }
        with open(f'train/metadata/metadata_v{self.config.version}.json', "w") as f:
            json.dump(self.metadata, f)

    def __save_model(self, model):
        version = self.config.version
        type = self.config.model.type
        identifier = self.config.model.identifier
        name = f'{type}_{identifier}_v{version}.dat'
        pickle.dump(model, open(f'models/{name}', "wb"))
        return name

    def get_model2(self, model2):
        model = xgb.XGBRegressor(
            n_estimators=27,
            max_depth=4,
            min_child_weight=1,
            eta=0.1,
            reg_lambda=0,
            objective='reg:squarederror',
            random_state=42)

        on_columns = []#self.config.features.on_columns
        windows = []#self.config.features.day_windows

        ct = ColumnTransformer([("selector", "passthrough", on_columns)],
                               verbose_feature_names_out=False,
                               remainder="drop").set_output(transform='pandas')

        return Pipeline([
            ("selector", ct),
            ('aggregator', FeatureAggregator(on_columns, windows)),
            ('scaler', StandardScaler()),
            ('model', model)
        ])
