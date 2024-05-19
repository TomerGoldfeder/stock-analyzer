import numpy as np
import pandas as pd


def rsi(data, period=30):
    """
    Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
    RSI oscillates between zero and 100. Traditionally and according to Wilder, RSI is considered overbought when above 70
    and oversold when below 30.

    Giving a large period will give a smoother RSI but will be less responsive to price changes.
    Large period - long term trading
    Small period - short term trading
    """
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def get_moving_avg(data: pd.DataFrame, window: int, column_to_use: str = "Close"):
    return data[column_to_use].rolling(window=window).mean()

def get_moving_avg_positivity(data: pd.DataFrame,
                              short_window: int = 30,
                              long_window: int = 200,
                              column_to_use: str = "Close"):
    return (get_moving_avg(data, short_window, column_to_use) /
            get_moving_avg(data, long_window, column_to_use))


def get_moving_positive_percentage(data, feature="moving_pos", threshold: float = 1.0):
    number_of_days_above_1 = len(data[data[feature] >= threshold])
    overall_positive = number_of_days_above_1 / len(data)
    return overall_positive

# macd technical indicator
def macd(data, short_window=50, long_window=200, signal_window=9):
    """
    Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship
    between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period EMA from
    the 12-period EMA. The result of that calculation is the MACD line. A nine-day EMA of the MACD called the "signal
    line," is then plotted on top of the MACD line, which can function as a trigger for buy and sell signals.

    The MACD is positive when the 12-day EMA is above the 26-day EMA and negative when the 12-day EMA is below the
    26-day EMA.
    """
    short_ema = data["Close"].ewm(span=short_window, adjust=False).mean()
    long_ema = data["Close"].ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    return macd_line, signal_line

# Accumulation/Distribution Line technical indicator
def accumulation_distribution_line(data):
    """
    The Accumulation/Distribution Line is a cumulative indicator that uses volume and price to assess whether a stock
    is being accumulated or distributed. The Accumulation/Distribution Line is a cumulative measure of each period's
    volume flow, or money flow. A high positive multiplier combined with high volume shows strong buying pressure that
    pushes the indicator higher. Conversely, a low negative number combined with high volume reflects strong selling
    pressure that pushes the indicator lower.
    """
    # adl = ((2 * data["Close"] - data["High"] - data["Low"]) /
    #        (data["High"] - data["Low"]) * data["Volume"]).cumsum()
    adl = pd.Series(0.0, index=data.index)
    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i-1]:
            adl[i] = adl[i-1] + ((data['Close'][i] - data['Low'][i]) / (data['High'][i] - data['Low'][i])) * data['Volume'][i]
        elif data['Close'][i] < data['Close'][i-1]:
            adl[i] = adl[i-1] - ((data['High'][i] - data['Close'][i]) / (data['High'][i] - data['Low'][i])) * data['Volume'][i]
        else:
            adl[i] = adl[i-1]
    return adl

# adx technical indicator
def adx(data, period=30):
    """
    The Average Directional Index (ADX) is used to measure the strength or weakness of a trend, not the actual direction.
    Directional movement is defined by +DI and -DI. The ADX measures the strength of a trend but not the direction.
    """
    #plus_di, minus_di = directional_movement_index(data, period=period)
    dx = 100 * abs(data['PLUS_DI'] - data['MINUS_DI']) / (data['PLUS_DI'] + data['MINUS_DI'])
    adx = dx.rolling(window=period).mean()
    return adx

# Directional Movement Index technical indicator
def directional_movement_index(d, period=30):
    """
    The Directional Movement Index (DMI) is a momentum indicator that was developed by J. Welles Wilder. It is used to
    determine the direction and strength of a trend. The DMI is composed of two lines, the Positive Directional Indicator
    (+DI) and the Negative Directional Indicator (-DI). The DMI is part of a series of technical indicators developed by
    Wilder, and some trading platforms split up the indicators, providing the Directional Movement as one indicator and
    the Average Direction Index (ADX) as another.
    """
    data = d.copy()
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = np.abs(data['High'] - data['Close'].shift())
    data['Low-PrevClose'] = np.abs(data['Low'] - data['Close'].shift())
    data['TR'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

    # Calculate directional movement
    data['UpMove'] = data['High'] - data['High'].shift()
    data['DownMove'] = data['Low'].shift() - data['Low']
    data['PlusDM'] = np.where((data['UpMove'] > data['DownMove']) & (data['UpMove'] > 0), data['UpMove'], 0)
    data['MinusDM'] = np.where((data['DownMove'] > data['UpMove']) & (data['DownMove'] > 0), data['DownMove'], 0)

    # Smoothed directional movement
    plus_di = 100 * (data['PlusDM'].rolling(window=period).mean() / data['TR'].rolling(window=period).mean())
    minus_di = 100 * (data['MinusDM'].rolling(window=period).mean() / data['TR'].rolling(window=period).mean())

    return plus_di, minus_di

# Stochastic Oscillator technical indicator
def stochastic_oscillator(data, period=30):
    """
    The Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the high-low
    range over a set number of periods. The Stochastic Oscillator is made up of two lines that range between 0 and 100.
    The %K line is usually displayed as a solid line and the %D line is usually displayed as a dotted line.
    """
    low_min = data["Low"].rolling(window=period).min()
    high_max = data["High"].rolling(window=period).max()
    k_percent = 100 * ((data["Close"] - low_min) / (high_max - low_min))
    d_percent = k_percent.rolling(window=3).mean()
    return k_percent, d_percent

def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    data["RSI"] = rsi(data)
    data["MACD"], data["SignalLine"] = macd(data)
    data["ADL"] = accumulation_distribution_line(data)
    data["PLUS_DI"], data["MINUS_DI"] = directional_movement_index(data)
    data["ADX"] = adx(data)
    data["K"], data["D"] = stochastic_oscillator(data)
    data["moving_pos"] = get_moving_avg_positivity(data)
    return data