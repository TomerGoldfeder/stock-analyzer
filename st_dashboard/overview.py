import streamlit as st
import pandas as pd


def overview():
    st.write("Stocks Overview")
    # Placeholder DataFrame
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': ['A', 'B', 'C', 'D']
    })
    st.dataframe(df)
