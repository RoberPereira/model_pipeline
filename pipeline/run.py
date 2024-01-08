from components._pipeline import Pipeline
import logging
import logging.config
import mlflow
from mlflow import MlflowClient


logging.config.fileConfig('../.logging.conf')
logger = logging.getLogger('Logger')

if __name__ == '__main__':

    #client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

    # Provide an Experiment description that will appear in the UI
    #experiment_description = ("Test run")

    # Provide searchable tags that define characteristics of the Runs that
    # will be in this Experiment
    #experiment_tags = {
    #    "project_name": "test-forecasting",
    #    "team": "rober-ml",
    #    "project_quarter": "Q4-2023",
    #    "mlflow.note.content": experiment_description,
    #}

    # Create the Experiment, providing a unique name
    #produce_apples_experiment = client.create_experiment(
    #    name="Test-Forecast", tags=experiment_tags
    #)

    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    apple_experiment = mlflow.set_experiment("Test-Forecast")
    mlflow.set_tag("mlflow.runName", "test-1")
    mlflow.autolog()

    pipeline = Pipeline()
    pipeline.run()
