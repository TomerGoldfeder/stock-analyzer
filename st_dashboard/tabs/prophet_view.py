import pandas as pd

from prophet_model.stock_model_prophet import ProphetPipeline
from st_dashboard.views_generators.prophet_views.get_prophet_output import get_prophet_output
import streamlit as st
import streamlit_shadcn_ui as ui


def stock_prophets_tab(stock_fetcher,
                       symbol,
                       start_date,
                       end_date,
                       predict_days):
    (history_stock_data,
     org_predicted_future_data,
     ground_truth_future_data,
     low_peaks_tuple,
     high_peaks_tuple), metrics = ProphetPipeline().exec_pipeline(stock_fetcher,
                                                                  symbol,
                                                                  start_date,
                                                                  end_date,
                                                                  predict_days)

    # present prophet
    prophet_fig = get_prophet_output(history_stock_data,
                                     org_predicted_future_data,
                                     ground_truth_future_data,
                                     low_peaks_tuple,
                                     high_peaks_tuple)
    present_prophet_model_performance(metrics, prophet_fig)


def present_prophet_model_performance(metrics: pd.DataFrame, prophet_fig):
    st.plotly_chart(prophet_fig, use_container_width=True)
#    with st.expander("Prophet Model Training And Prediction Metrics"):
    metrics_col = st.columns(len(metrics.columns.values))

    for i, col_name in enumerate(metrics.columns.values):
        with metrics_col[i]:
            ui.metric_card(title=col_name,
                           content=metrics.iloc[0][col_name],
                           key=col_name)