from src.services.loaderclass import StockLoader
from src.services.featureclass import FeatureEngineering
from src.services.transformerclass import Transformer
from src.utils.model_functions import interpolate_prediction_days
from . import train_metadata

import pickle
import io
import base64

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import joblib

sns.set_theme(color_codes=True)
plt.switch_backend('Agg')

__model = None


def forecast():

    startdate = dt.datetime(2023, 1, 1)
    enddate = dt.datetime(2023, 12, 1)
    forecast_dt = dt.datetime(2023, 10, 10)

    df_stock = load_stock('MELI', startdate, enddate)

    return np.round(get_forecast(df_stock.loc[forecast_dt:,]
                                 .iloc[0:1]).tolist(), 2).tolist()


def get_forecast(ds_forecast):

    features = train_metadata.etl_metadata.features
    fe = FeatureEngineering()
    ds_forecast = fe.compute_lag_features(ds_forecast)

    return __model.predict(ds_forecast[features])


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
    # ds_forecast_result = pd.read_pickle('data/v0.0.1/processed/
    # xgb_meli_ds_forecast_2023-10-15.pkl')
    startdate = dt.datetime(2023, 1, 1)
    enddate = dt.datetime(2023, 12, 1)
    forecast_dt = dt.datetime(2023, 10, 11)

    ds_stock = load_stock('MELI', startdate, enddate)

    ds_forecast = pd.DataFrame(get_forecast(ds_stock[:]),
                               index=ds_stock.index)
    ds_forecast = ds_forecast.loc[forecast_dt:].iloc[0:1,].to_numpy()

    dt_forecast_idx = get_forecast_idx(forecast_dt)

    ds_forecast_interpolate = interpolate_prediction_days(ds_forecast[0],
                                                          dt_forecast_idx,
                                                          [1, 5, 10, 23])
    
    ds_forecast_result = pd.concat([ds_stock[startdate:][['close', 'open']],
                                    ds_forecast_interpolate], axis=0)

    df_update = ds_forecast_result.astype(float)


    # df_update = pd.concat([df_update, ds_forecast_result[['forecast', 
    #                                                      'forecast_upp_b',
    #                                                      'forecast_low_b']]],
    #                      axis=1)

    fig, axs = plt.subplots(1, figsize=(15, 5))
    df_update['2023-01-05':][['open', 'forecast']].plot(ax=axs)

    # Save the chart as animage (e.g., PNG)
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
