import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import streamlit as st


class Analyzer():
    def __init__(self, stock_data: pd.DataFrame, predictions: pd.DataFrame):
        self.stock_data = stock_data
        self.predictions = predictions

    def validate_inputs(self):
        if self.stock_data.empty or self.predictions.empty:
            st.write("Dataframes are empty")
            return False
        if self.stock_data.shape[0] != self.predictions.shape[0]:
            st.write("Dataframes have different number of rows")
            return False
        return True
    def evaluate(self) -> pd.DataFrame:
        if not self.validate_inputs():
            return pd.DataFrame({"mae": [0], "mse": [0], "rmse": [0]})
        mae = mean_absolute_error(self.stock_data['y'], self.predictions['yhat'])
        mse = mean_squared_error(self.stock_data['y'], self.predictions['yhat'])
        rmse = np.sqrt(mse)

        return pd.DataFrame({"mae": [mae], "mse": [mse], "rmse": [rmse]})