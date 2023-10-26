from src.services.loaderclass import StockLoader
from src.services.targetdefinerclass import TargetDefiner
import pandas as pd
import datetime as dt
import logging
import joblib

logger = logging.getLogger('Logger')


class MethodResult:

    def __init__(self, method) -> None:
        self.method = method
        self.data = pd.DataFrame()
        self.metadata = {}

    def get_method(self):
        return self.method

    def set_data(self, data: pd.DataFrame):
        self.data = data

    def get_data(self) -> pd.DataFrame:
        return self.data

    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_metadata(self) -> dict:
        return self.metadata

    def save_metadata(self) -> None:
        pass


class ComponentMethod:

    def __init__(self, version, params, method) -> None:
        self.version = version
        self.method = method
        self.params = params
        self.mresult = MethodResult(self.method)

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        pass

    def save_mresult(self, path_name):
        joblib.dump(self.mresult.get_data(), f'data/{path_name}_v{self.version}_{dt.datetime.now().timestamp()}')


class Extract(ComponentMethod):

    def __init__(self, version, params) -> None:
        """ Initialize extractor method.
        Parameters:
            params (Dict): method execution parameters.
            required values : {
                "stock": "MELI",
                "startdate": "1990-01-01",
                "enddate": "2023-10-11"
            }
        """
        super().__init__(version, params, 'extract')
        self.stock = params.get('stock')
        self.startdate = dt.datetime.strptime(params.get('startdate'), '%Y-%m-%d')
        self.enddate = dt.datetime.strptime(params.get('enddate'), '%Y-%m-%d')

    def execute(self,  last_results: list[MethodResult]) -> MethodResult:
        """ Execute extraction.
        Parameters:
            last_result (dict): Result of last execution step.
        Returns:
            MethodResult: Data extraction.
        """
        logger.info(f'Extracting data. {self.params}')
        sloader = StockLoader(self.stock)
        data = sloader.load_stock(self.startdate, self.enddate)
        self.mresult.set_data(data)
        self.mresult.set_metadata(self.params)
        self.save_mresult()
        logger.info(f'Done extracting data. {self.params}')
        return self.mresult

    def save_mresult(self):
        s_date = self.startdate.strftime("%Y:%m:%d")
        e_date = self.enddate.strftime("%Y:%m:%d")
        path_name = f'raw/{self.stock}_{s_date}_{e_date}'
        super().save_mresult(path_name)


class Trasnform(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(params, version, 'transform')

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        """ Execute data transformation.
        Parameters:
            last_result (dict): Result of last execution step.
        Returns:
            MethodResult: Data transformed.
        """
        logger.info(f"Execute data transformation. {self.params}")
        last_result = last_results[-1]
        self.mresult.set_data(last_result.get_data())
        self.mresult.set_metadata(self.params)
        return self.mresult


class ComputeTarget(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'compute_target')

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        """ Compute target.
        Parameters:
            last_result (MethodResult): Result of last execution step.
                data (pd.DataFrame): data from the last step
                metada (dict): metadata from last step
        Returns:
            MethodResult: Data from trarget execution.
        """
        logger.info(f"Execute target computation. {self.params}")
        tdefiner = TargetDefiner(self.params)
        last_result = last_results[-1]
        data = tdefiner.compute_target(last_result.get_data())
        self.mresult.set_data(data)
        self.mresult.set_metadata(self.params)
        return self.mresult


class Load(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(version, params, 'load')
        self.path_name = params.get('path_name')

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        logger.info(f"Execute load for training and anaytics. {self.params}")

        if self.path_name:
            pass
            # Load Data from path
            # Save data on mresult
        else:
            extract_result = [result for result in last_results if result.get_method() == 'extract'][0]
            print('EL TYPE', type(extract_result))
            params = extract_result.get_metadata()
            s_date = params.get('startdate')
            e_date = params.get('enddate')
            self.path_name = f'processed/{params.get("stock")}_{s_date}_{e_date}'

            last_result = last_results[-1]
            self.mresult.set_data(last_result.get_data())
            self.mresult.set_metadata(self.params)

        self.save_mresult(self.path_name)
        logger.info(f"Done loading data for training and anaytics. {self.params}")
