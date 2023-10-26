from ._mthdcomponents import (ComponentMethod, MethodResult)
import logging

logger = logging.getLogger('Logger')


class DataSplitter(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(params, version, 'data_splitter')

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        logger.info(f'Execute Data Splitter. {self.params}')
        pass


class ModelBuilder(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(params, version, 'model')

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        logger.info(f'Getting Model. {self.params}')
        pass


class ModelTrainer(ComponentMethod):

    def __init__(self, version, params) -> None:
        super().__init__(params, version, 'model_trainer')

    def execute(self, last_results: list[MethodResult]) -> MethodResult:
        logger.info(f'Execute Model train. {self.params}')
        pass
