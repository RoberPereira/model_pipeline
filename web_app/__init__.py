from flask import Flask


def build_app():
    app = Flask(__name__)

    from . import routes
    app.register_blueprint(routes.app)

    from . import predictor
    predictor.load_model()
    predictor.load_artifacts()

    return app
