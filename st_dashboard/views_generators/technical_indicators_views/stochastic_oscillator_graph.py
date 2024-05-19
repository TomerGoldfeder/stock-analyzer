import numpy as np
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit_shadcn_ui as ui

def present_stochastic_oscillator_graph(data: pd.DataFrame):
    k_data = data['K']
    d_data = data['D']
    stochastic_oscillator_labels = data['stochastic_oscillator_label']

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2,
                        print_grid=True)

    # Add traces for the first subplot
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['Close'],
                             mode='lines',
                             name='Close Price',
                             line=dict(color='blue')),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=data.index,
                             y=[80]*data.shape[0],
                             mode='lines',
                             name='Near High Range',
                             line=dict(color='green'),
                             fill='tozeroy',
                             fillcolor='rgba(0, 255, 0, 0.1)'),
                    row=2, col=1)

    fig.add_hline(y=80, line_dash="dash", line_color="green", row=2, col=1,
                  opacity=0.1,
                  annotation_text="High Stock Price", annotation_position="top left")

    fig.add_trace(go.Scatter(x=data.index,
                             y=[20]*data.shape[0],
                             mode='lines',
                             name='Near Low Range',
                             line=dict(color='red'),
                             fill='tozeroy',
                             fillcolor='rgba(255, 255, 255, 1)'),
                  row=2, col=1)

    fig.add_hline(y=20, line_dash="dash", line_color="red", row=2, col=1,
                  opacity=0.1,
                    annotation_text="Low Stock Price", annotation_position="bottom left")


    # Add traces for the second subplot
    fig.add_trace(go.Scatter(x=data.index,
                             y=k_data,
                             mode='lines',
                             name='K',
                             line=dict(color='orange')),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=data.index,
                                y=d_data,
                                mode='lines',
                                name='D',
                                line=dict(color='purple')),
                    row=2, col=1)

    # Update layout
    fig.update_layout(height=700, width=800, title_text="Stochastic Oscillator Over Time",
                      hovermode="x unified")

    # Update x-axis labels
    fig.update_xaxes(title_text="Date", row=2, col=1)
    # Update y-axis labels
    fig.update_yaxes(title_text="Close Price", row=1, col=1)
    fig.update_yaxes(title_text="Stochastic Oscillator", row=2, col=1)

    with st.expander("Stochastic Oscillator Details"):
        k_mean, d_mean = np.mean(k_data), np.mean(d_data)
        stoc_oscillator_mean = np.mean([k_mean, d_mean])
        ui.metric_card(title="Stochastic Oscillator", content=f"{round(stoc_oscillator_mean, 4)}",
                       description='K & D averaged over selected dates', key="stochastic_oscillator")
        st.plotly_chart(fig, use_container_width=True)