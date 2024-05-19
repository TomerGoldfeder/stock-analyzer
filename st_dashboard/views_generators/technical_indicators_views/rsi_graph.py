import pandas as pd
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit_shadcn_ui.py_components as ui


def present_rsi_graph(data: pd.DataFrame):
    rsi_data = data['RSI']
    rsi_labels = data['rsi_label']

    # setting lower and upper bounds for RSI
    lower_bound = 30
    upper_bound = 70

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
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
                             y=rsi_data,
                             mode='lines',
                             name='RSI',
                             line=dict(color='orange')),
                  row=2, col=1)
    # adding boundaries
    fig.add_hline(y=lower_bound, line_dash='dash', line_color='red', line_width=1,
                  row=2, col=1)
    fig.add_hline(y=upper_bound, line_dash='dash', line_color='green', line_width=1,
                  row=2, col=1)

    # Update layout
    fig.update_layout(height=600, width=800, title_text="RSI Over Time",
                      showlegend=True, hovermode="x unified")

    # Update x-axis labels
    fig.update_xaxes(title_text="Date", row=2, col=1)

    # Update y-axis labels
    fig.update_yaxes(title_text="Close Price", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)

    with st.expander("RSI Details"):
        ui.metric_card(title="RSI", content=rsi_data.mean(),
                       description='RSI averaged over selected dates', key="rsi")

        st.plotly_chart(fig, use_container_width=True)