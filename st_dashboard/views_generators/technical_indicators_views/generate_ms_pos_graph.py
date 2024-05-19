import numpy as np
import plotly.graph_objects as go


def generate_ma_pos_graph(relative_ma, feature):

    y_below_1 = np.where(relative_ma[feature] < 1, relative_ma[feature], 1)  # Cap values above 1 to 1
    y_above_1 = np.where(relative_ma[feature] > 1, relative_ma[feature], 1)  # Cap values below 1 to 1

    # Create layout
    layout = go.Layout(
        title='Positivity Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Positivity'),
        hovermode="x unified"
    )

    # Create traces for the area below and above 1
    area_below_1 = go.Scatter(
        x=relative_ma.index,
        y=y_below_1,
        mode='lines',
        fill='tonexty',  # Fill area to y=0
        fillcolor='rgba(255, 255, 255, 1)',  # white color
        name='Negative',
        # line with light red color
        line=dict(color='rgba(242, 38, 19, 1)')

    )

    area_above_1 = go.Scatter(
        x=relative_ma.index,
        y=y_above_1,
        mode='lines',
        fill='tonexty',  # Fill area to y=0
        fillcolor='rgba(46, 204, 113, 0.4)',  # Light green color
        name='Positive',
        # line with light green color
        line=dict(color='rgba(22, 160, 133, 1)')
    )

    positive_area = go.Scatter(
        x=relative_ma.index,
        y=[1]* relative_ma.shape[0],
        mode='lines',
        name='Positive Threshold',
        line=dict(color='rgba(0, 0, 0, 1)'),
        fill='tonexty',
        fillcolor='rgba(22, 160, 133, 1)'
    )

    fig = go.Figure(data=[area_below_1, area_above_1, positive_area],layout=layout)

    # Set range for y-axis based on data points
    fig.update_yaxes(range=[min(1, relative_ma[feature].min()), max(1, relative_ma[feature].max())])

    return fig