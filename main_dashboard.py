import streamlit as st
from prophet_model.stock_model_prophet import StockModelProphet
from st_dashboard.stock_analysis import stock_analysis
from st_dashboard.overview import overview
import streamlit_shadcn_ui as ui
st.set_page_config(page_title="Stock Analyzer", layout="wide")


# Main function to run the app
def main():
    st.title("Stock Analyzer Dashboard")
    tabs = ["Overview", "Stock Analysis"]
    all_tabs = ui.tabs(tabs, tabs[0])
    if all_tabs == "Overview":
        overview()
    elif all_tabs == "Stock Analysis":
        stock_analysis()


if __name__ == "__main__":
    main()
