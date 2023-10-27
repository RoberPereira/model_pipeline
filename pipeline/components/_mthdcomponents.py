from sklearn.pipeline import Pipeline
import pandas as pd
import joblib


class MethodResult:

    def __init__(self, method) -> None:
        self.method = method
        self.datasets = {str: pd.DataFrame}
        self.pipeline = None
        self.metadata = {}

    def get_method(self):
        return self.method

    def set_dataset(self, data: pd.DataFrame, name='data'):
        self.datasets[name] = data

    def get_dataset(self, name='data') -> pd.DataFrame:
        return self.datasets[name]

    def set_pipeline(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def get_pipeline(self) -> Pipeline:
        return self.pipeline

    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_metadata(self) -> dict:
        return self.metadata


class ComponentMethod:

    def __init__(self, version, params, method='generic') -> None:
        self.version = version
        self.method = method
        self.params = params
        self.mresult = MethodResult(self.method)

    def execute(self, last_results: list) -> MethodResult:
        pass

    def save_mresult_data(self, path_name):
        joblib.dump(self.mresult.get_dataset(), f'data/{path_name}_v{self.version}')

    def save_mrresult(self):
        pass

    def find_result(self, last_results: list, method: str) -> MethodResult:
        return [r for r in last_results if [k for k in r.values() if k == method]][0]
