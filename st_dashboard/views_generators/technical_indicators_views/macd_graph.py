import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import streamlit_shadcn_ui.py_components as ui



def present_macd_graph(data: pd.DataFrame):
    macd_data = data['MACD']
    signal_line = data['SignalLine']

    fig = go.Figure()

    # calculate diff between macd and signal line
    # add trace of bar histogram of the diff between MACD and Signal Line
    data['MACD_Hist'] = data['MACD'] - data['SignalLine']

    fig.add_trace(go.Bar(x=data[data['MACD_Hist'] > 0].index,
                         y=data[data['MACD_Hist'] > 0]['MACD_Hist'],
                         name='MACD Positive Histogram',
                         marker={'color': 'green',
                                 'opacity': 0.4}))
    fig.add_trace(go.Bar(x=data[data['MACD_Hist'] <= 0].index,
                         y=data[data['MACD_Hist'] <= 0]['MACD_Hist'],
                         name='MACD Negative Histogram',
                         marker={'color': 'red',
                                 'opacity': 0.4},
                         ))

    # Add traces for the first subplot
    fig.add_trace(go.Scatter(x=data.index,
                             y=macd_data,
                             mode='lines',
                             name='MACD',
                             line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index,
                             y=signal_line,
                             mode='lines',
                             name='Signal Line',
                             line=dict(color='orange')))

    # Update layout
    fig.update_layout(height=600, width=800, title_text="MACD Over Time",
                      showlegend=True, hovermode="x unified")

    # Update x-axis labels
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="MACD -  12 Short   /   26 Long   /   9 Signal Line")

    window = 30
    last_30_days_rolling_histogram = data['MACD_Hist'].rolling(window=window).mean()[-1]
    line_slope = (data['MACD_Hist'].diff(window) / window)[-1]

    signal_crossing = np.where((macd_data > signal_line) & (macd_data.shift(1) <= signal_line.shift(1)), 1,
                               np.where((macd_data < signal_line) & (macd_data.shift(1) >= signal_line.shift(1)), -1,
                                        0)).sum()

    last_macd_value = macd_data.iloc[-1]
    if last_macd_value > 0:
        bullish_bearish = "Bullish"
    elif last_macd_value < 0:
        bullish_bearish = "Bearish"
    else:
        bullish_bearish = "Neutral"

    with st.expander("MACD Details"):
        col_1, col_2 = st.columns(2)
        # have a 2 by 2 matrix to display the metrics
        with col_1:
            ui.metric_card(title="Bullish/Bearish", content=bullish_bearish,
                           description='Current MACD Status', key="bullish_bearish")
            ui.metric_card(title="MACD Slope", content=line_slope,
                           description='Slope of MACD over selected dates (30 days window)', key="macd_slope")

        with col_2:
            ui.metric_card(title="Signal Line", content=str(signal_crossing),
                           description='Number of times MACD crossed Signal Line', key="signal_crossing")
            ui.metric_card(title="MACD", content=last_30_days_rolling_histogram,
                           description='MACD averaged selected dates (30 days window)', key="macd")

        st.plotly_chart(fig, use_container_width=True)