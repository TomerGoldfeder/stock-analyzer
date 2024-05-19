import pandas as pd


class MovingAVG:

    @staticmethod
    def get_moving_avg(data:pd.DataFrame, short_window: int, long_window: int, feature: str):
        data[feature] = (data['Close'].rolling(window=short_window).mean() /
                         data['Close'].rolling(window=long_window).mean())
        return data

    @staticmethod
    def get_positive_percentage(data, feature):
        number_of_days_above_1 = len(data[data[feature] >= 1])
        number_of_days_below_1 = len(data[data[feature] < 1])
        overall_positive = number_of_days_above_1 / (number_of_days_above_1 + number_of_days_below_1)
        return overall_positive
