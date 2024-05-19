from algo.get_moving_avg_pos import get_ma_pos
from st_dashboard.views_generators.technical_indicators_views.generate_ms_pos_graph import generate_ma_pos_graph
from st_dashboard.views_generators.technical_indicators_views.get_buy_sell_graph import get_buy_sell_graph
from st_dashboard.views_generators.technical_indicators_views.adl_graph import present_adl_graph
from st_dashboard.views_generators.technical_indicators_views.adx_graph import present_adx_graph
from st_dashboard.views_generators.technical_indicators_views.macd_graph import present_macd_graph
from st_dashboard.views_generators.technical_indicators_views.positivity_graph import present_positivity_metrics
from st_dashboard.views_generators.technical_indicators_views.rsi_graph import present_rsi_graph
from st_dashboard.views_generators.technical_indicators_views.stochastic_oscillator_graph import \
    present_stochastic_oscillator_graph
from technical_indicators.label_model.label_model import train_predict_label_model
import streamlit as st
import streamlit_shadcn_ui as ui
from technical_indicators.label_model.labeling_functions import apply_lfs
from technical_indicators.technical_indicators import calculate_technical_indicators


def technical_indicators_tab(symbol, stock_fetcher, start_date, end_date):
    # train and predict with label model
    historical_data = stock_fetcher.fetch_raw_data(start_date, end_date)
    labels = calculate_technical_indicators(historical_data)
    applied_labeling_functions = apply_lfs(labels)
    labels = train_predict_label_model(applied_labeling_functions=applied_labeling_functions)

    # moving average and positivity
    feature, relative_ma_df, positivity = get_ma_pos(symbol, org_start=start_date, org_end=end_date)
    ######################################################

    # presenting all results
    ######################################################

    # present high level decisions
    present_high_level_decisions(labels)
    # present buy sell windows
    present_buy_sell_graph(labels)
    present_supporting_decisions(labels)
    # present moving average and positivity
    present_technical_indicators(applied_labeling_functions, relative_ma_df, feature, positivity)

def present_buy_sell_graph(labels):
    buy_sell_graph = get_buy_sell_graph(labels)
    st.plotly_chart(buy_sell_graph, use_container_width=True)


def get_windowed_buy_sell_ratio(labels, window_size=7):
    last_x_days = labels.iloc[-window_size:]
    last_x_days_buys = last_x_days[last_x_days['preds'] == 1]
    last_x_days_sells = last_x_days[last_x_days['preds'] == 0]
    overall_sell_or_buy = "Buy" if last_x_days_buys.shape[0] > last_x_days_sells.shape[0] else "Sell"
    if overall_sell_or_buy == "Buy":
        overall_strenght_of_decision = round(last_x_days_buys.shape[0] / last_x_days.shape[0], 5)
    else:
        overall_strenght_of_decision = round(last_x_days_sells.shape[0] / last_x_days.shape[0], 5)
    return overall_sell_or_buy, overall_strenght_of_decision


def present_high_level_decisions(labels):
    # st.header("High Level Decisions")
    col1, col2, col3 = st.columns(3, gap='medium')
    with col1:
        ui.metric_card(title="Latest Buy/Sell Decision", content=decode_predictions(labels['preds'].iloc[-1]),
                       description=str(labels['preds_proba'].iloc[-1]), key="last_pred")
    with col2:
        last_7_days_sell_or_buy, last_7_days_strenght_of_decision = get_windowed_buy_sell_ratio(labels, 7)
        ui.metric_card(title="Buy / Sell Ratio Over Last 7 Days", content=str(last_7_days_sell_or_buy),
                          description=last_7_days_strenght_of_decision, key="buy_sell_ratio_7_days")
    with col3:
        last_30_days_sell_or_buy, last_30_days_strenght_of_decision = get_windowed_buy_sell_ratio(labels, 30)
        ui.metric_card(title="Buy / Sell Ratio Over Last 30 Days", content=str(last_30_days_sell_or_buy),
                          description=last_30_days_strenght_of_decision, key="buy_sell_ratio_30_days")

def present_supporting_decisions(labels):
    with st.expander("Supporting Metrics for the Latest Decision"):
        col1, col2, col3 = st.columns(3, gap='medium')

        with col1:
            ui.metric_card(title="RSI With 30 Days Window", content=decode_predictions(labels['rsi_label'].iloc[-1]),
                           description=labels['RSI'].iloc[-1], key="rsi_label")
            ui.metric_card(title="MACD", content=decode_predictions(labels['macd_label'].iloc[-1]),
                              description='Latest', key="macd_label")
        with col2:
            ui.metric_card(title="ADL", content=decode_predictions(labels['adl_label'].iloc[-1]),
                                description='Latest', key="adl_label")
            ui.metric_card(title="ADX", content=decode_predictions(labels['adx_label'].iloc[-1]),
                                description='Latest', key="adx_label")
        with col3:
            ui.metric_card(title="Stochastic Oscillator With 30 Days Window", content=decode_predictions(labels['stochastic_oscillator_label'].iloc[-1]),
                                description='Latest', key="stochastic_oscillator_label")
            ui.metric_card(title="Positivity", content=str(round(labels['moving_pos'].iloc[-1], 5)),
                                description='Latest', key="pos_label")


def present_technical_indicators(applied_labeling_functions, relative_ma_df, feature, positivity):
    present_positivity_metrics(positivity, generate_ma_pos_graph(relative_ma_df, feature))
    present_rsi_graph(applied_labeling_functions)
    present_macd_graph(applied_labeling_functions)
    present_adl_graph(applied_labeling_functions)
    present_adx_graph(applied_labeling_functions)
    present_stochastic_oscillator_graph(applied_labeling_functions)


def decode_predictions(pred):
    if pred == -1:
        return "Do Nothing"
    elif pred == 1:
        return "Buy"
    else: return "Sell"