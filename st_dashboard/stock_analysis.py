import datetime
import streamlit as st

from stock_fetcher.stock_fetcher import StockFetcher
from st_dashboard.tabs.performance_against_index import present_performance_against_index
from st_dashboard.tabs.technical_indicators import technical_indicators_tab
from st_dashboard.tabs.prophet_view import stock_prophets_tab
from streamlit_extras.stateful_button import button


def stock_analysis():
    # Input fields
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)
    with st.sidebar.expander("Inputs", expanded=True):
        symbol = st.text_input("Enter Symbol:", value="SPY")
        start_date = st.text_input("Enter Start Date (YYYY-MM-DD):", value=start_date.strftime("%Y-%m-%d"))
        end_date = st.text_input("Enter End Date (YYYY-MM-DD):", value=end_date.strftime("%Y-%m-%d"))
        predict_days = st.number_input("Predict Future Days:", min_value=1, step=1)
        based_on_index = st.text_input("Base Index", placeholder="e.g: GSPC for S&P 500")
        submit_button = button("Submit", key="submit_button")

    if submit_button:
        # Call function to handle the analysis
        navigate_tabs(symbol, start_date, end_date, predict_days, based_on_index)


def navigate_tabs(symbol, start_date, end_date, predict_days, based_on_index):
    tabs_options = ["Stock Prophets", "Technical Indicators", "Performance Against Index"]
    tabs = st.tabs(tabs_options)
    stock_fetcher = StockFetcher(symbol)
    with tabs[0]: # Stock Prophets
        stock_prophets_tab(stock_fetcher,
                           symbol,
                           start_date,
                           end_date,
                           predict_days)
    with tabs[1]: # Technical Indicators
        technical_indicators_tab(symbol, stock_fetcher, start_date, end_date)
    with tabs[2]: # Performance Against Index
        if based_on_index:
            present_performance_against_index(symbol, based_on_index, start_date, end_date)
        else:
            st.warning("Please provide a base index")




