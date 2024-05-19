from technical_indicators.evaluate_product import ProductEvaluator
import streamlit as st
import streamlit_shadcn_ui as ui


def present_performance_against_index(symbol, index_key, start_date, end_date):
    columns_to_calculate = ['Close', 'Adj Close']
    tracking_error, etf_returns, index_returns = ProductEvaluator(symbol, index_key).evaluate(start_date, end_date,
                                                                                              columns=columns_to_calculate)



    close_col, adj_close_col = st.columns(len(columns_to_calculate))

    with close_col:
        ui.metric_card(title="Return", content=tracking_error['Close'],
                       description='Close', key="close")

    with adj_close_col:
        ui.metric_card(title="Return", content=tracking_error['Adj Close'],
                       description='Adj Close', key="adj_close")

    with st.expander("Tracking Error Details"):
        # Divide the screen into two columns
        etf_col, index_col = st.columns(2)

        # Place dataframes within the columns
        with etf_col:
            st.write(f"<b>{symbol} Return</b>", unsafe_allow_html=True)
            st.write(etf_returns)

        with index_col:
            st.write(f"<b>{index_key} Return</b>", unsafe_allow_html=True)
            st.write(index_returns)