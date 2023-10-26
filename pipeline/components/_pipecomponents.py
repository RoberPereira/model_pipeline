from components._mthdcomponents import (ComponentMethod, Extract, Trasnform,
                                        ComputeTarget, Load)
import logging

logger = logging.getLogger('Logger')


class PipelineComponent:

    def __init__(self, params) -> None:
        self.params = params
        pass

    def run(self):
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
        elif (params.get('method') == 'compute_target'):
            return ComputeTarget(self.version, params.get('params'))
        elif (params.get('method') == 'load'):
            return Load(self.version, params.get('params'))

    def run(self):
        """ Rinning ETL process. """
        steps = self.params.get('steps')
        logger.info(f"Running Etl process. {[i['method'] for i in steps]}")

        results = []
        for step in steps:
            result = self.get_method(step).execute(results)
            results.append(result)

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


class Train(PipelineComponent):
    """ Train execution component. """

    def __init__(self, params) -> None:
        self.version = params.get('version')
        super().__init__(params)

    def get_method(self, params) -> ComponentMethod:
        if (params.get('method') == 'extract'):
            return Extract(self.version, params.get('params'))
        elif (params.get('method') == 'transform'):
            return Trasnform(self.version, params.get('params'))
        elif (params.get('method') == 'compute_target'):
            return ComputeTarget(self.version, params.get('params'))
        elif (params.get('method') == 'load'):
            return Load(self.version, params.get('params'))

    def run(self):
        """ Rinning ETL process. """
        steps = self.params.get('steps')
        logger.info(f"Running Etl process. {[i['method'] for i in steps]}")

        results = []
        for step in steps:
            result = self.get_method(step).execute(results)
            results.append(result)
