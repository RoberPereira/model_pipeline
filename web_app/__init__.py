from src.utils.util import DotDict
from flask import Flask
import json

with open('web_app/config.json', 'r') as f:
    config = DotDict(**json.load(f))

train_version = config.train_version
with open(f'train/metadata/metadata_v{train_version}.json', 'r') as f:
    train_metadata = DotDict(**json.load(f))


def build_app():
    app = Flask(__name__)

    from . import routes
    app.register_blueprint(routes.app)

    from . import predictor
    predictor.load_model()

    return app
