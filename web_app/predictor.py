from src.services.loaderclass import StockLoader
from src.utils.model_functions import interpolate_prediction_days

import pickle
import io
import base64

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt

sns.set_theme(color_codes=True)
plt.switch_backend('Agg')

__model = None


def forecast():

    startdate = dt.datetime(2023, 1, 1)
    enddate = dt.datetime(2023, 12, 1)
    forecast_dt = dt.datetime(2023, 10, 10)

    df_stock = load_stock('MELI', startdate, enddate)
    return np.round(get_forecast(df_stock, forecast_dt).to_list(), 2).tolist()


def get_forecast(ds: pd.DataFrame, forecast_dt) -> pd.DataFrame:
    return pd.DataFrame(__model.predict(ds),
                        index=ds.index).loc[forecast_dt]


def load_model():
    print('Loading model...')
    global __model
    if __model is None:
        __model = pickle.load(
            open("models/xgb_meli_one_v01.dat", "rb"))

    print('Model loaded successfully')


def load_stock(stock, startdate, enddate):

    loader = StockLoader(stock)
    ds_stock = loader.load_stock(startdate, enddate)

    return ds_stock


def get_forecast_idx(forecast_dt: dt):
    return pd.bdate_range(start=forecast_dt,
                          periods=23, freq='B')


def generate_forecast_chart():

    startdate = dt.datetime(2023, 1, 1)
    enddate = dt.datetime(2023, 12, 1)
    forecast_dt = dt.datetime(2023, 10, 10)

    ds_stock = load_stock('MELI', startdate, enddate)

    ds_forecast_result = get_forecast_result(startdate, forecast_dt, ds_stock)

    fig, axs = plt.subplots(1, figsize=(15, 5))
    ds_forecast_result['2023-01-05':][['open', 'forecast']].plot(ax=axs)

    # Save the chart as animage (e.g., PNG)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode()
    plt.close()  # Close the plot to free up resources

    return chart_image


def get_forecast_result(startdate, forecast_dt, ds_stock):

    ds_forecast = get_forecast(ds_stock, forecast_dt).to_numpy()
    dt_forecast_idx = get_forecast_idx(forecast_dt)

    ds_forecast_interpolate = interpolate_prediction_days(ds_forecast,
                                                          dt_forecast_idx,
                                                          [1, 5, 10, 23])

    ds_forecast_result = pd.concat([ds_stock[startdate:][['close', 'open']],
                                    ds_forecast_interpolate], axis=0)

    return ds_forecast_result.astype(float)
