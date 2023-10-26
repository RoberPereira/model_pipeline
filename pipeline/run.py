from components._pipecomponents import (
    PipelineComponent,
    Etl)
import logging
import logging.config
import json


logging.config.fileConfig('../.logging.conf')
logger = logging.getLogger('Logger')


def get_component(params) -> PipelineComponent:
    if (params.get('type') == 'etl'):
        return Etl(params)
    # elif (params.get('type') == 'train'):
    #    return Train(params)


if __name__ == '__main__':

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    for pipe_step in config.get('steps'):

        logger.info(f'Start pipeline step : {pipe_step.get("type")}')
        get_component(pipe_step).run()

    #logger.debug('debug message')
    #logger.info('info message')
    #logger.warning('warn message')
    #logger.error('error message')
    #logger.critical('critical message')

