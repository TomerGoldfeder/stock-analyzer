import pandas as pd
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit_shadcn_ui.py_components as ui

not_trending = 20
confirmed_trending = 40
strong_trending = 50
extremely_strong_trending = 70


def get_adx_trend(current_adx):
    if current_adx < not_trending:
        adx_trend = "Not Trending"
    elif current_adx < confirmed_trending:
        adx_trend = "Confirmed Trending"
    elif current_adx < strong_trending:
        adx_trend = "Strong Trending"
    elif current_adx < extremely_strong_trending:
        adx_trend = "Very Strong Trending"
    else:
        adx_trend = "Rare Strong Trending"

    return adx_trend

def decode_labels_into_decision(label):
    if label == 1:
        return "Buy"
    elif label == 0:
        return "Sell"
    else:
        return "Do Nothing"

def present_adx_graph(data: pd.DataFrame):
    adx_data = data['ADX']
    adx_labels = data['adx_label']

    minus_di = data['MINUS_DI']
    plus_di = data['PLUS_DI']

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2,
                        print_grid=True)

    # Add traces for the first subplot
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['Close'],
                             mode='lines',
                             name='Close Price',

                             line=dict(color='blue')),
                  row=1, col=1)

    # Add traces for the second subplot
    fig.add_trace(go.Scatter(x=data.index,
                             y=adx_data,
                             mode='lines',
                             name='ADX',
                             line=dict(color='red')),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=data.index,
                             y=minus_di,
                             mode='lines',
                             name='-DI',
                             line=dict(color='lightblue')),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=data.index,
                             y=plus_di,
                             mode='lines',
                             name='+DI',
                             line=dict(color='orange')),
                  row=2, col=1)

    # adding boundaries
    # setting lower and upper bounds for RSI

    fig.add_hline(y=not_trending, line_dash='dash', line_color='yellow', line_width=1,
                  row=2, col=1,
                  opacity=0.4,
                  name="Not Trending",
                  annotation_text="Not Trending",
                  annotation_position='top left')
    fig.add_hline(y=confirmed_trending, line_dash='dash', line_color='green', line_width=1,
                  row=2, col=1,
                  opacity=0.4,
                  name="Confirmed Trending",
                  annotation_text="Confirmed Trending",
                  annotation_position='top left')
    fig.add_hline(y=strong_trending, line_dash='dash', line_color='purple', line_width=1,
                  row=2, col=1,
                  opacity=0.4,
                  name="Strong Trending",
                  annotation_text="Strong Trending",
                  annotation_position='top left')
    fig.add_hline(y=extremely_strong_trending, line_dash='dash', line_color='red', line_width=1,
                  row=2, col=1,
                  opacity=0.4,
                  name="Rare Strong Trending",
                  annotation_text="Rare Strong Trending",
                  annotation_position='top left')
    # Update layout
    fig.update_layout(height=700, width=800, title_text="ADX Over Time",
                      showlegend=True, hovermode="x unified")

    # Update x-axis labels
    fig.update_xaxes(title_text="Date", row=2, col=1)

    # Update y-axis labels
    fig.update_yaxes(title_text="Close Price", row=1, col=1)
    fig.update_yaxes(title_text="ADX", row=2, col=1)

    # last 30 days average of ADX
    last_30_days_average_adx = adx_data.rolling(window=30).mean()[-1]
    adx_trend = get_adx_trend(adx_data.iloc[-1])

    with st.expander("ADX Details"):
        col_1, col_2 = st.columns(2)
        # have a 2 by 2 matrix to display the metrics
        with col_1:
            ui.metric_card(title="ADX", content=last_30_days_average_adx,
                           description='ADX averaged over selected dates (30 days window)', key="adx_30_days")

        with col_2:
            ui.metric_card(title="Current ADX Trend", content=adx_trend,
                           description=adx_data.iloc[-1], key="current_adx")

        st.plotly_chart(fig, use_container_width=True)