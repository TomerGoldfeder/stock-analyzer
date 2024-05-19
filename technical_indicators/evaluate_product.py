from typing import Union

import numpy as np
from stock_fetcher.stock_fetcher import StockFetcher


class ProductEvaluator:
    def __init__(self, product: str, following_index: str):
        self.product: str = product
        self.following_index: str = f"^{following_index}"
        self.product_stock_fetcher = StockFetcher(self.product)
        self.index_stock_fetcher = StockFetcher(self.following_index)

    def fetch_product_data(self, start_date: str, end_date: str):
        return self.product_stock_fetcher.fetch_raw_data(start_date, end_date)

    def fetch_index_data(self, start_date: str, end_date: str):
        return self.index_stock_fetcher.fetch_raw_data(start_date, end_date)

    def compute_difference(self, product_data, index_data):
        etf_returns = product_data.pct_change().dropna()
        index_returns = index_data.pct_change().dropna()
        return etf_returns, index_returns

    def get_tracking_error(self, etf_returns, index_returns, columns: Union[str, list] = 'Close'):
        # Compute tracking error (standard deviation of the difference in returns)
        tracking_error = np.std(etf_returns - index_returns)
        return tracking_error[columns]

    def evaluate(self, start_date: str, end_date: str, columns: Union[str, list] = 'Close'):
        index_data = self.fetch_index_data(start_date=start_date, end_date=end_date)
        product_data = self.fetch_product_data(start_date=start_date, end_date=end_date)
        etf_returns, index_returns = self.compute_difference(product_data, index_data)
        tracking_error = self.get_tracking_error(etf_returns, index_returns, columns)
        return tracking_error, etf_returns, index_returns
