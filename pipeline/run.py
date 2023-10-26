from src.classes.pipelineclass import PipelineStep
from etl.etl import Etl
from train.train import Train
import logging
import logging.config
import json


logging.config.fileConfig('../.logging.conf')
logger = logging.getLogger('Logger')


def get_step_class(params) -> PipelineStep:
    if (params.get('type') == 'etl'):
        return Etl(params)
    elif (params.get('type') == 'train'):
        return Train(params)


if __name__ == '__main__':

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    for pipe_step in config.get('steps'):

        logger.info(pipe_step.get('type'))
        pipe_class = get_step_class(pipe_step)

        for class_step in pipe_step.get('steps'):

            class_method = getattr(pipe_class, class_step.get('method'))
            result = class_method(class_step.get('params'))

            print(result)

        

    #logger.debug('debug message')
    #logger.info('info message')
    #logger.warning('warn message')
    #logger.error('error message')
    #logger.critical('critical message')

