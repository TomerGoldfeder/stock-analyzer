import plotly.graph_objects as go

def get_prophet_output(history_stock_data, org_predicted_future_data, ground_truth_future_data, low_peaks_tuple, high_peaks_tuple):
    # Plot historical and future data
    fig = plot_forecast(history_stock_data, org_predicted_future_data, ground_truth_future_data, low_peaks_tuple, high_peaks_tuple)
    return fig

def plot_forecast(data, forecast, ground_truth_future_data, low_peaks: tuple, high_peaks: tuple):
    fig = go.Figure()

    # Confidence interval
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        mode='lines',
        name='Upper Bound',
        line=dict(color='#b8e2f2'),
        visible="legendonly",
        opacity=0.2
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        mode='lines',
        name='Lower Bound',
        fill='tonexty',
        fillcolor='#b8e2f2',
        visible="legendonly",
        opacity=0.3
    ))

    fig.add_trace(go.Scatter(
        x=low_peaks[0],
        y=low_peaks[1],
        mode='lines',
        name='Peaks Low',
        line=dict(color='red'),
        visible="legendonly",
        opacity=0.2
    ))

    fig.add_trace(go.Scatter(
        x=high_peaks[0],
        y=high_peaks[1],
        mode='lines',
        name='Peaks High',
        line=dict(color='green'),
        visible="legendonly",
        opacity=0.3
    ))

    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['trend'],
        mode='lines',
        name='Trend',
        line=dict(color='rgba(0,255,0,0.2)'),
        visible="legendonly",
        opacity=0.6
    ))

    # Original data
    fig.add_trace(go.Scatter(
        x=data['ds'],
        y=data['y'],
        mode='lines',
        name='Actual',
        line=dict(color='#00008B')
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        mode='lines',
        name='Forecast',
        line=dict(color='rgb(255, 213, 128)')
    ))

    # GT future
    fig.add_trace(go.Scatter(
        x=ground_truth_future_data['ds'],
        y=ground_truth_future_data['y'],
        mode='lines',
        name='GT Future',
        line=dict(color='#bea9fd')
    ))

    # Layout
    fig.update_layout(title='Prophet Forecast',
                      xaxis_title='Date',
                      yaxis_title='Prediction')

    return fig
