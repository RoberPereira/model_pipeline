from sklearn.pipeline import Pipeline
import pandas as pd
import joblib


class MethodResult:

    def __init__(self, method) -> None:
        self.method = method
        self.status = None
        self.input_params = {}
        self.output = {}
        self.datasets = {str: pd.DataFrame}
        self.pipeline = None

    def get_method(self):
        return self.method

    def set_method(self, method):
        self.method = method

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def set_input_params(self, metadata):
        self.input_params = metadata

    def get_input_params(self) -> dict:
        return self.input_params

    def get_output(self):
        return self.output

    def set_output(self, output):
        self.output = output

    def add_dataset(self, data: pd.DataFrame, name='data'):
        self.datasets[name] = data

    def get_dataset(self, name='data') -> pd.DataFrame:
        return self.datasets[name]

    def get_datasets(self) -> {str: pd.DataFrame}:
        return self.datasets

    def set_datasets(self, datasets):
        self.datasets = datasets

    def set_pipeline(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def get_pipeline(self) -> Pipeline:
        return self.pipeline


class PipelineMethod:

    def __init__(self, version, params, method) -> None:
        self.version = version
        self.method = method
        self.params = params
        self.mresult = MethodResult(self.method)

    def execute(self, last_results: list) -> MethodResult:
        pass

    def save_mresult_data(self, path_name, data_name='data'):
        joblib.dump(self.mresult.get_dataset(data_name), f'pipeline/data/{path_name}_v{self.version}')

    def passthrough(self, in_params, output, status,
                    datasets: {str: pd.DataFrame} = None,
                    pipeline=None):
        self.mresult.set_input_params(in_params)
        self.mresult.set_output(output)
        self.mresult.set_status(status)
        self.mresult.set_pipeline(pipeline)
        self.mresult.set_datasets(datasets)

    def previews_restult(self, last_results: list):
        return last_results[-1].get('result')

    def find_result(self, last_results: list, method: str) -> MethodResult:
        return [r for r in last_results if [k for k in r.values() if k == method]][0]
