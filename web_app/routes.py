from flask import render_template, Blueprint, jsonify
from . import predictor


# Create a Blueprint for routes
app = Blueprint('web_app', __name__)


@app.route('/')
def index():
    return "Welcome to the Home Page"


@app.route('/ping')
def hello():
    return 'pong'
# render_template('index.html')


@app.route('/forecast', methods=['GET'])
def forecast():

    response = jsonify({
        'forecast': predictor.forecast()
    })
    return response


@app.route('/forecast_render', methods=['GET'])
def forecast_render():

    chart_image = predictor.generate_forecast_chart()
    return render_template('chart.html', chart_image=chart_image)
