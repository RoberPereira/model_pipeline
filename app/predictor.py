import pickle
import joblib

import matplotlib.pyplot as plt
import io
import base64

from pandas_datareader import data as pdr
import yfinance as yf

import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
dt.datetime.strptime

sns.set_theme(color_codes=True)
yf.pdr_override()
plt.switch_backend('Agg')

__forecast = None
__model = None


def forecast():
    return np.round(__model.predict(__forecast).tolist(), 2).tolist()


def load_artifacts():
    print('Loading artifacts...')

    global __forecast
    if __forecast is None:
        __forecast = joblib.load("data/processed/X_forecast")

    print('Artifacts loaded successfully')


def load_model():
    print('Loading model...')

    global __model
    if __model is None:
        __model = pickle.load(
            open("models/xgb_pipeline_MELI_10-15.dat", "rb"))

    print('Model loaded successfully')


def stock_update():
    startdate = dt.datetime(2023, 1, 1)
    enddate = dt.datetime(2023, 12, 1)

    df_update = pdr.get_data_yahoo('MELI', start=startdate, end=enddate)

    df_update.columns = df_update.columns.str.lower()
    return df_update


def generate_forecast_chart():
    ds_forecast_result = pd.read_pickle('data/processed/xgb_meli_ds_forecast_2023-10-15.pkl')

    df_update = stock_update()
    df_update = pd.concat([df_update, ds_forecast_result[['forecast', 
                                                          'forecast_upp_b',
                                                          'forecast_low_b']]],
                                                          axis=1)

    fig, axs = plt.subplots(1, figsize=(15, 5))
    df_update['2023-01-05':][['open', 'forecast']].plot(ax=axs)

    # Save the chart as an image (e.g., PNG)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode()
    plt.close()  # Close the plot to free up resources

    return chart_image


def generate_chart():
    # Create your chart using Matplotlib
    plt.plot([1, 2, 3, 4])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Save the chart as an image (e.g., PNG)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode()
    plt.close()  # Close the plot to free up resources

    return chart_image


if __name__ == "__main__":
    load_model()
