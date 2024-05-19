import numpy as np
from snorkel.labeling import labeling_function

# Define constants for labeling
BUY = 1
SELL = 0
DO_NOTHING = -1

# Labeling functions based on technical indicators
@labeling_function()
def rsi_label(row):
    if row['RSI'] is None or np.isnan(row['RSI']).all():
        return DO_NOTHING
    if row['RSI'] < 30:
        return BUY
    elif row['RSI'] > 70:
        return SELL
    else:
        return DO_NOTHING

@labeling_function()
def macd_label(row):
    if row['MACD'] > row['SignalLine']:
        return BUY
    elif row['MACD'] < row['SignalLine']:
        return SELL
    else:
        return DO_NOTHING

# Accumulation/Distribution Line labeling function
@labeling_function()
def adl_label(row):
    if row['ADL'] > 0:
        return BUY
    elif row['ADL'] < 0:
        return SELL
    else:
        return DO_NOTHING

# adx labeling function
@labeling_function()
def adx_label(row):
    """
    When +DI is above -DI and ADX is rising, it suggests a strong uptrend.
    when -DI is above +DI and ADX is rising, it indicates a strong downtrend.
    Currently when the ADX is below 25, we wouldn't want to try and predict a trend.
    :param row:
    :return:
    """
    if row['ADX'] is None or np.isnan(row['ADX']).all() or \
            row['PLUS_DI'] is None or np.isnan(row['PLUS_DI']).all() or \
            row['MINUS_DI'] is None or np.isnan(row['MINUS_DI']).all():
        return DO_NOTHING
    if row['PLUS_DI'] > row['MINUS_DI'] and row['ADX'] > ((row['PLUS_DI'] + row['MINUS_DI']) / 2):
        return BUY
    elif row['MINUS_DI'] > row['PLUS_DI'] and row['ADX'] > ((row['PLUS_DI'] + row['MINUS_DI']) / 2):
        return SELL
    else:
        return DO_NOTHING

# stochastic_oscillator labeling function
@labeling_function()
def stochastic_oscillator_label(row):
    if row['K'] is None or np.isnan(row['K']).all() or \
            row['D'] is None or np.isnan(row['D']).all():
        return DO_NOTHING
    oversold = 20
    overbought = 80
    if row['K'] < oversold and row['D'] < oversold:
        return BUY
    elif row['K'] > overbought and row['D'] > overbought:
        return SELL
    elif oversold < row['K'] < overbought and oversold < row['D'] < overbought:
        return BUY
    else:
        return DO_NOTHING

def get_labeling_functions():
    return [rsi_label, macd_label, adl_label, adx_label, stochastic_oscillator_label]

def apply_lfs(labels):
    labels['rsi_label'] = labels.apply(rsi_label, axis=1)
    labels['macd_label'] = labels.apply(macd_label, axis=1)
    labels['adl_label'] = labels.apply(adl_label, axis=1)
    labels['adx_label'] = labels.apply(adx_label, axis=1)
    labels['stochastic_oscillator_label'] = labels.apply(stochastic_oscillator_label, axis=1)
    return labels
