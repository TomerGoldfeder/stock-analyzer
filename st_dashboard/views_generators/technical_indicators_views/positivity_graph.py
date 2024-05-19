import streamlit as st
import streamlit_shadcn_ui.py_components as ui


def present_positivity_metrics(positivity: dict, positivity_graph):
    with st.expander("Positivity Details"):
        pos_col, pos_relative_col = st.columns(len(list(positivity.keys())))

        with pos_col:
            ui.metric_card(title="Positivity", content=positivity['pos'],
                           description='Over Last 2K days', key="pos")

        with pos_relative_col:
            ui.metric_card(title="Positivity", content=positivity['pos_dates'],
                           description='Over Selected Dates', key="pos_relative")

        st.plotly_chart(positivity_graph, use_container_width=True)