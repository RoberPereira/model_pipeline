from pipeline.components._pipemethods import (PipelineMethod)
from pipeline.components._etlmethods import (Extract, Trasnform, Load)
from pipeline.components._trainmethods import (LoadEtl, ComputeFeatures,
                                               ComputeTarget, DataSplitter,
                                               ModelBuilder, ModelTrainer, SaveModel)
import json
import logging

logger = logging.getLogger('Logger')


class PipelineStep:

    def __init__(self, params) -> None:
        self.params = params
        pass

    def run(self, step_results: list) -> list:
        """ Rinning pipeline process. """
        steps = self.params.get('steps')
        logger.info(f"Running pipeline process. {[i['method'] for i in steps]}")

        for step in steps:
            result = self.get_method(step).execute(step_results)
            step_results.append({'method': step.get('method'), 'result': result})
        return step_results

    def save_result(self):
        pass


class Etl(PipelineStep):
    """ ETL execution component. """

    def __init__(self, params) -> None:
        self.version = params.get('version')
        super().__init__(params)

    def get_method(self, params) -> PipelineMethod:
        method = params.get('method')
        if (method == 'extract'):
            return Extract(self.version, params.get('params'), method)
        elif (method == 'transform'):
            return Trasnform(self.version, params.get('params'), method)
        elif (method == 'load'):
            return Load(self.version, params.get('params'), method)


class Train(PipelineStep):
    """ Train execution component. """

    def __init__(self, params) -> None:
        self.version = params.get('version')
        super().__init__(params)

    def get_method(self, params) -> PipelineMethod:
        method = params.get('method')
        if (method == 'load_etl'):
            return LoadEtl(self.version, params.get('params'), method)
        elif (method == 'compute_target'):
            return ComputeTarget(self.version, params.get('params'), method)
        elif (method == 'compute_features'):
            return ComputeFeatures(self.version, params.get('params'), method)
        elif (method == 'data_split'):
            return DataSplitter(self.version, params.get('params'), method)
        elif (method == 'build_model'):
            return ModelBuilder(self.version, params.get('params'), method)
        elif (method == 'train'):
            return ModelTrainer(self.version, params.get('params'), method)
        elif (method == 'save_model'):
            return SaveModel(self.version, params.get('params'), method)


class Pipeline:

    def __init__(self) -> None:
        with open('pipeline/config.json', 'r') as config_file:
            self.config = json.load(config_file)
        self.version = self.config.get('version')

    def get_step(self, params) -> PipelineStep:
        if (params.get('type') == 'etl'):
            return Etl(params)
        elif (params.get('type') == 'train'):
            return Train(params)

    def run(self):
        results = []
        for step in self.config.get('steps'):
            logger.info(f'Start pipeline step : {step.get("type")}')
            results.extend(self.get_step(step).run(results))      
        self.save_history(results)

    def save_history(self, results):
        history = {}
        for r in results:
            result = r.get('result')
            method = result.get_method()

            history[method] = {
                'status': result.get_status(),
                'input_params': result.get_input_params(),
                'output': result.get_output()
            }
            model_name = ''
            if method == 'save_model':
                model_name = result.get_output().get('model_name')
                model_features = result.get_pipeline()['aggregator'].agg_features_
                history[method]['model_features'] = model_features

        with open(f'pipeline/history/{model_name}_{self.version}.json', "w") as file:
            json.dump(history, file)
