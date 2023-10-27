"""

from src.model_functions import compute_evaluation_metrics
from src.services.splitterclass import DataSplitterCustom
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


''' def __save_metadata(self, fe, raw_file, precessed_file):
    self.metadata = {
        'etl_version': self.version,
        'stock': self.stock,
        'startdate': self.startdate.strftime("%Y:%m:%d"),
        'endddate': self.enddate.strftime("%Y:%m:%d"),
        'output_raw': raw_file,
        'output_processed': precessed_file,
        'target': fe.get_target_columns()
    }
    with open(f'etl/metadata/metadata_v{self.version}.json', "w") as file:
        json.dump(self.metadata, file) '''


class Train():

    def __init__(self, config) -> None:
        self.config = config

    def run(self, parmas):
        print('Start training...')                    

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
"""
