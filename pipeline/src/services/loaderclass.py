from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
import pandas as pd


class StockLoader():

    def __init__(self, stock) -> None:
        yf.pdr_override()
        self.stock = stock

    def load_stock(self, startdate: dt, enddate: dt) -> pd.DataFrame:
        df = pdr.get_data_yahoo(self.stock, start=startdate, end=enddate)
        df.columns = df.columns.str.lower()
        return df


if __name__ == '__main__':

    loader = StockLoader('MELI')
    df = loader.load_stock(dt.datetime(1990, 1, 1),
                           dt.datetime(2023, 10, 11))

    print(df.info())
