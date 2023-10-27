from components._pipecomponents import (
    PipelineComponent, Etl, Train)
import logging
import logging.config
import json


logging.config.fileConfig('../.logging.conf')
logger = logging.getLogger('Logger')


def get_component(params) -> PipelineComponent:
    if (params.get('type') == 'etl'):
        return Etl(params)
    elif (params.get('type') == 'train'):
        return Train(params)


if __name__ == '__main__':

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    retults = []
    for pipe_step in config.get('steps'):
        logger.info(f'Start pipeline step : {pipe_step.get("type")}')
        retults.extend(get_component(pipe_step).run())
