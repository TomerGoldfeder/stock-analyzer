import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit_shadcn_ui.py_components as ui



def present_adl_graph(data: pd.DataFrame):
    close_price_data = data['Close']
    adl_data = data['ADL']
    adl_labels = data['adl_label']

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index,
                             y=close_price_data,
                             mode='lines',
                             name='Close Price',
                             line=dict(color='blue')))

    min_range = close_price_data.min() - 1
    max_range = close_price_data.max() + 1
    # Normalize the data to the range of -2 to 2
    adl_min_range = adl_data.min()
    adl_max_range = adl_data.max()

    normalized_adl_data = ((adl_data - adl_min_range) / (adl_max_range - adl_min_range)) * (
                max_range - min_range) + min_range

    fig.add_trace(go.Scatter(x=data.index,
                             y=normalized_adl_data,
                             mode='lines',
                             name='ADL',
                             line=dict(color='orange')))

    fig.update_layout(height=600, width=800, title_text="ADL Over Time",
                      showlegend=True, hovermode="x unified")

    # Update x-axis labels
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="ADL")

    change_of_rate = (adl_data.pct_change(5) * 100)[-1]

    last_adl_value = adl_data.iloc[-1]
    previous_adl_value = adl_data.iloc[-2]
    if last_adl_value > previous_adl_value:
        adl_trend = "Accumulation"
    elif last_adl_value < previous_adl_value:
        adl_trend = "Distribution"
    else:
        adl_trend = "No significant trend"

    with st.expander("ADL Details"):
        col_1, col_2 = st.columns(2)
        # have a 2 by 2 matrix to display the metrics
        with col_1:
            ui.metric_card(title="ADL Change of Rate", content=change_of_rate,
                           description='Change of rate over selected dates (5 days window)', key="adl_change")
        with col_2:
            ui.metric_card(title="ADL Trend", content=adl_trend,
                           description=last_adl_value, key="adl_trend")

        st.plotly_chart(fig, use_container_width=True)