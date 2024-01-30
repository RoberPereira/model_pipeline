from ._pipemethods import (PipelineMethod, MethodResult)
from pipeline.src.services.loaderclass import StockLoader
import datetime as dt
import logging

logger = logging.getLogger('Logger')


class Extract(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)
        self.stock = params.get('stock')
        self.startdate = dt.datetime.strptime(params.get('startdate'), '%Y-%m-%d')
        self.enddate = dt.datetime.strptime(params.get('enddate'), '%Y-%m-%d')

    def execute(self,  last_results: list) -> MethodResult:
        '''Execute extraction.'''

        logger.info(f'Extracting data. {self.params}')
        sloader = StockLoader(self.stock)
        data = sloader.load_stock(self.startdate, self.enddate)

        s_date = self.startdate.strftime("%Y-%m-%d")
        e_date = self.enddate.strftime("%Y-%m-%d")
        path_name = f'raw/{self.stock}_{s_date}_{e_date}'

        output = {'output_raw': path_name}
        self.passthrough(self.params, output, 'succes', {'data': data})
        self.save_mresult_data(path_name)
        logger.info(f'Done extracting data. {self.params}')
        return self.mresult


class Trasnform(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(params, version, method)

    def execute(self, last_results: list) -> MethodResult:
        '''Execute data transformation.'''
        logger.info(f"Execute data transformation. {self.params}")

        self.passthrough(self.params, {}, 'succes',
                         last_results[-1].get('result').get_datasets())
        return self.mresult


class Load(PipelineMethod):

    def __init__(self, version, params, method) -> None:
        super().__init__(version, params, method)
        self.path_name = params.get('path_name')

    def execute(self, last_results: list) -> MethodResult:
        logger.info(f"Execute load for training and anaytics. {self.params}")

        if self.path_name:
            pass
            # Load Data from path
            # Save data on mresult
        else:
            extract_result = self.find_result(last_results, 'extract').get('result')
            params = extract_result.get_input_params()
            s_date = params.get('startdate')
            e_date = params.get('enddate')
            self.path_name = f'processed/{params.get("stock")}_{s_date}_{e_date}'

        output = {'output_processed': self.path_name}
        self.passthrough(self.params, output, 'succes', last_results[-1].get('result').get_datasets())
        self.save_mresult_data(self.path_name)

        logger.info(f"Done loading data for training and anaytics. {self.params}")
        return self.mresult
