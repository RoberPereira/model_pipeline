from components._pipeline import Pipeline
import logging
import logging.config
import mlflow
from mlflow import MlflowClient


logging.config.fileConfig('../.logging.conf')
logger = logging.getLogger('Logger')

if __name__ == '__main__':



    pipeline = Pipeline()
    pipeline.run()
