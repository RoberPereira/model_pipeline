from src.classes.pipelineclass import PipelineStep
from src.utils.util import DotDict
from src.services.loaderclass import StockLoader
from src.services.targetdefinerclass import TargetDefiner
import logging
import datetime as dt
import joblib
import json


logger = logging.getLogger('Logger')


class Etl(PipelineStep):

    metadata = {}

    def __init__(self, config) -> None:
        self.config = config
        self.version = config.get('version')
        # self.stock = config.fetch_data.stock
        # self.startdate = dt.datetime.strptime(config.fetch_data.startdate,
        #                                      '%Y-%m-%d')
        # self.enddate = dt.datetime.strptime(config.fetch_data.enddate,
        #                                    '%Y-%m-%d')

    def fetch_data(self, params):

        print(f'Fetching {params.get("stock")} stock data')
        pass

    def compute_target(self, params):

        print(f'Compute traget on columns {params.get("on_column")},'
              + f'forecat days: {params.get("forecast_day")}')
        pass



    def run(self):
        logger.info("run etl")

        for step in self.config.get('steps'):

            method = step.get('method')
            params = step.get('params')
            logger.info(f'Running {method}...')

            # exec(f"self.{method}", params)

    '''
    def run(self):

        print(f'Fetching {self.stock} stock data')
        sl = StockLoader(self.stock)
        ds_stock_data = sl.load_stock(self.startdate, self.enddate)

        print('Saving raw data...')
        raw_file = self.__save_data(ds_stock_data, self.stock,
                                    self.startdate, self.enddate,
                                    'raw')

        print('Computing target')
        fe = TargetDefiner(self.config.compute_target)
        ds_stock_data = fe.compute_target(ds_stock_data)

        print('Saving processed data...')
        processed_file = self.__save_data(ds_stock_data, self.stock,
                                          self.startdate, self.enddate,
                                          'processed')

        print('Saving metadata')
        self.__save_metadata(fe, raw_file, processed_file)

        print('End Etl successfully')        
    '''

    def __save_metadata(self, fe, raw_file, precessed_file):
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
            json.dump(self.metadata, file)

    def __save_data(self, ds, stock, startdate, enddate, folder):

        s_date = startdate.strftime("%Y:%m:%d")
        e_date = enddate.strftime("%Y:%m:%d")
        name = f'{stock}_{s_date}_{e_date}_v{self.version}'
        joblib.dump(ds, f'data/{folder}/{name}')
        return name


if __name__ == '__main__':

    etl = Etl()
    etl.run()
