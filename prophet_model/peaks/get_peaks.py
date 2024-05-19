import pandas as pd
import numpy
import typing
from scipy.signal import find_peaks


class PeakFinder:
    def __init__(self, stock_symbol:str, stock_data: pd.DataFrame):
        self.stock_symbol = stock_symbol
        self.stock_data = stock_data
        self.high_peaks_widths = None
        self.low_peaks_width = None
        self.high_peaks = None
        self.lower_peaks = None

    def combine_peaks(self) -> typing.Optional[typing.List[pd.Timestamp]]:
        if not self.high_peaks.size and not self.lower_peaks.size:
            return None
        all_peaks = numpy.concatenate((self.lower_peaks, self.high_peaks))
        rows = self.stock_data.iloc[all_peaks]
        rows['ds'] = pd.to_datetime(rows['ds'], format='%Y-%m-%d')
        rows = rows.sort_values(by='ds')
        return rows['ds']

    def get_high_low_peaks(self) -> typing.Tuple[numpy.ndarray, numpy.ndarray]:
        series = self.stock_data['y']

        max_prominence = 0.5
        distance = 5  # 1 sample per day * 30 days * 3 months
        self.high_peaks, _ = find_peaks(series,
                                       prominence=max_prominence,
                                       distance=distance)
        self.lower_peaks, _ = find_peaks(-series,
                                        prominence=max_prominence,
                                        distance=distance)
        return self.high_peaks, self.lower_peaks
