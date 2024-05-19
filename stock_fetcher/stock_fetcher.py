import yfinance as yf
import pandas as pd
from yfinance import Ticker


class StockFetcher():
    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol

    def fetch_data_by_period(self, period="max") -> pd.DataFrame:
        ticker = Ticker(self.stock_symbol)
        stock_data = ticker.history(period=period)
        return self.preprocess_data(stock_data)

    def fetch_raw_data(self, start_date: str, end_date: str):
        print(f"[START] Fetching data [stock={self.stock_symbol}] [start_date={start_date}] [end_date={end_date}]")
        stock_data = yf.download(self.stock_symbol, start=start_date, end=end_date)
        print(
            f"[END] data [stock={self.stock_symbol}] [start_date={start_date}] [end_date={end_date}] [rows={len(stock_data)}]")
        return stock_data
    def fetch_data_by_time_range(self,
                                 start_data: str,
                                 end_date: str) -> pd.DataFrame:
        stock_data = self.fetch_raw_data(start_date=start_data, end_date=end_date)
        return self.preprocess_data(stock_data)

    @staticmethod
    def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
        data.reset_index(inplace=True)
        data = data.rename(columns={"Date": "ds", "Adj Close": "y"})
        return data

    def fetch_gt_future_data(self, history_stock_data, org_predicted_future_data):
        start_data = history_stock_data['ds'].max()
        end_date = org_predicted_future_data['ds'].max()
        return self.fetch_data_by_time_range(start_data=start_data,
                                             end_date=end_date)

