from components._mthdcomponents import (ComponentMethod)
from components._etlcomponents import (Extract, Trasnform, Load)
from components._traincomponents import (LoadEtl, ComputeFeatures, ComputeTarget,
                                         DataSplitter, ModelBuilder, ModelTrainer,
                                         SaveModel)
import logging

logger = logging.getLogger('Logger')


class PipelineComponent:

    def __init__(self, params) -> None:
        self.params = params
        self.results = []
        pass

    def run(self) -> list:
        """ Rinning pipeline process. """
        steps = self.params.get('steps')
        logger.info(f"Running pipeline process. {[i['method'] for i in steps]}")

        for step in steps:
            result = self.get_method(step).execute(self.results)
            self.results.append({'method': step.get('method'), 'result': result})
        return self.results

    def save_result(self):
        pass


class Etl(PipelineComponent):
    """ ETL execution component. """

    def __init__(self, params) -> None:
        self.version = params.get('version')
        super().__init__(params)

    def get_method(self, params) -> ComponentMethod:
        if (params.get('method') == 'extract'):
            return Extract(self.version, params.get('params'))
        elif (params.get('method') == 'transform'):
            return Trasnform(self.version, params.get('params'))
        elif (params.get('method') == 'load'):
            return Load(self.version, params.get('params'))


class Train(PipelineComponent):
    """ Train execution component. """

    def __init__(self, params) -> None:
        self.version = params.get('version')
        super().__init__(params)

    def get_method(self, params) -> ComponentMethod:
        if (params.get('method') == 'load_etl'):
            return LoadEtl(self.version, params.get('params'))
        elif (params.get('method') == 'compute_target'):
            return ComputeTarget(self.version, params.get('params'))
        elif (params.get('method') == 'compute_features'):
            return ComputeFeatures(self.version, params.get('params'))
        elif (params.get('method') == 'data_split'):
            return DataSplitter(self.version, params.get('params'))
        elif (params.get('method') == 'build_model'):
            return ModelBuilder(self.version, params.get('params'))
        elif (params.get('method') == 'train'):
            return ModelTrainer(self.version, params.get('params'))
        elif (params.get('method') == 'save_model'):
            return SaveModel(self.version, params.get('params'))
