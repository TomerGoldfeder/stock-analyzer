import typing
import pandas as pd
from prophet import Prophet

from prophet_model.peaks.get_peaks import PeakFinder
from prophet_model.performance_analyzer.analyzer import Analyzer
from stock_fetcher.stock_fetcher import StockFetcher

pd.set_option('display.max_columns', None)


class StockModelProphet:
    def __init__(self, model: typing.Any = None,
                 daily_seasonality: int = False,
                 weekly_seasonality: int = True,
                 yearly_seasonality: int = True,
                 change_points: typing.List = None):
        self.daily_seasonality = daily_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.yearly_seasonality = yearly_seasonality
        self.change_points = change_points
        self.model = self.init_model(model)

    def init_model(self, model):
        if model is not None:
            return model
            # seasonality_prior_scale=0.1, holidays_prior_scale=10.0, changepoint_prior_scale=0.05
        model = Prophet(# changepoint_prior_scale=0.05,
                        # seasonality_prior_scale=30,
                        interval_width=0.8,
                        daily_seasonality=self.daily_seasonality,
                        weekly_seasonality=self.weekly_seasonality,
                        yearly_seasonality=self.yearly_seasonality,
                        changepoints=self.change_points)
        return model

    def get_stock_model(self) -> typing.Any:
        return self.model

    def fit(self, stock_data: pd.DataFrame) -> None:
        self.model.fit(stock_data)

    def make_predict_future(self, days: int) -> pd.DataFrame:
        future = self.model.make_future_dataframe(periods=days, include_history=True)
        forecast = self.model.predict(future)
        return forecast

    def fit_predict(self, stock_data: pd.DataFrame, days: int) -> pd.DataFrame:
        self.fit(stock_data)
        return self.make_predict_future(days)


class ProphetPipeline:
    def prophet_train_predict(self, stock_fetcher: StockFetcher,
                              selected_company,
                              start_date,
                              end_date,
                              num_future_days):
        history_stock_data = stock_fetcher.fetch_data_by_time_range(start_date, end_date)

        ######################################################
        # get high and low peaks from the historical data
        peak_finder = PeakFinder(selected_company, history_stock_data)
        high_peaks, low_peaks = peak_finder.get_high_low_peaks()

        ######################################################
        # Fetch techincal indicators

        ######################################################
        # for AAPL - daily - True, weekly - False, yearly - True + peaks
        # for INTC - daily - True, weekly - False, yearly - True + peaks
        # for MSFT - daily - True, weekly - False, yearly - True + peaks
        stock_model_prophet = StockModelProphet(change_points=peak_finder.combine_peaks(),
                                                daily_seasonality=True,
                                                weekly_seasonality=False)
        # Fit the model
        stock_model_prophet.fit(stock_data=history_stock_data)
        ######################################################
        # predict future data
        org_predicted_future_data = stock_model_prophet.make_predict_future(days=num_future_days)
        ######################################################
        # Fetch actual future data
        ground_truth_future_data = stock_fetcher.fetch_gt_future_data(history_stock_data=history_stock_data,
                                                                      org_predicted_future_data=org_predicted_future_data)
        ######################################################

        ######################################################
        # get high & lows
        plot_x_low = [] if not low_peaks.size else history_stock_data.loc[low_peaks]['ds']
        plot_y_low = [] if not low_peaks.size else history_stock_data.loc[low_peaks]['y']
        plot_x_high = [] if not high_peaks.size else history_stock_data.loc[high_peaks]['ds']
        plot_y_high = [] if not high_peaks.size else history_stock_data.loc[high_peaks]['y']
        low_peaks_tuple = (plot_x_low, plot_y_low)
        high_peaks_tuple = (plot_x_high, plot_y_high)
        return history_stock_data, org_predicted_future_data, ground_truth_future_data, low_peaks_tuple, high_peaks_tuple

    def analyze_performance(self,
                            org_predicted_future_data,
                            ground_truth_future_data):
        predicted_future_data_for_analyzing = org_predicted_future_data[
            org_predicted_future_data['ds'].isin(ground_truth_future_data['ds'])]
        ######################################################
        # Evaluate the model
        ######################################################
        print("evaluating prophet model...")
        metrics: pd.DataFrame = (Analyzer(ground_truth_future_data,
                                         predicted_future_data_for_analyzing)
                                 .evaluate())
        print("prophet model evaluated...")
        return metrics

    def exec_pipeline(self,
                      stock_fetcher: StockFetcher,
                      selected_company,
                      start_date,
                      end_date,
                      num_future_days):
        (history_stock_data,
         org_predicted_future_data,
         ground_truth_future_data,
         low_peaks_tuple,
         high_peaks_tuple) = self.prophet_train_predict(stock_fetcher,
                                                        selected_company,
                                                        start_date,
                                                        end_date,
                                                        num_future_days)
        metrics = self.analyze_performance(org_predicted_future_data, ground_truth_future_data)

        return ((history_stock_data,
                org_predicted_future_data,
                ground_truth_future_data,
                low_peaks_tuple,
                high_peaks_tuple),
                metrics)

