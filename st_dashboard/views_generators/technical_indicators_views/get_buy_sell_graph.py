import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from technical_indicators.label_model.labeling_functions import get_labeling_functions




def generate_hover_text(labels):
    labels['preds_trans'] = labels['preds'].apply(lambda x: 'Buy' if x == 1 else 'Sell' if x == 0 else 'Do Nothing')
    labels['dates'] = labels.index
    labels['confidence'] = labels['preds_proba']
    labeling_functions_names = ['dates', 'preds_trans', 'confidence']
    labeling_functions_names += [x.name for x in get_labeling_functions()]
    labels['hover_text'] = labels[labeling_functions_names].apply(lambda x: [f"{'#'*6+'<br>' if i == 3 else ''}{labeling_functions_names[i]}: {x[labeling_functions_names[i]]}" for i in range(len(x))], axis=1)
    labels['hover_text'] = labels['hover_text'].apply(lambda x: "<br>".join(x))

    return labels


def get_opacities_based_on_confidence(labels):
    opacity_thresholds = [0.80, 0.90, 0.9999]
    opacities = []
    for i in range(labels['preds'].shape[0]):
        if labels['preds_proba'].iloc[i] < opacity_thresholds[0]:
            opacities.append(0.2)
        elif labels['preds_proba'].iloc[i] < opacity_thresholds[1]:
            opacities.append(0.4)
        elif labels['preds_proba'].iloc[i] < opacity_thresholds[2]:
            opacities.append(0.8)
        else:
            opacities.append(1)
    return opacities

def get_buy_sell_graph(labels):
    # Define colors for each category
    values_to_categories = {1: 'Buy', 0: 'Sell', -1: 'Do Nothing'}
    # Create traces for each category

    sell_content = labels[labels['preds'] == 0] # should be 0
    buy_content = labels[labels['preds'] == 1] # should be 1
    do_nothing_content = labels[labels['preds'] == -1]

    # filter out
    sell_content = sell_content[sell_content['preds_proba'] > 0.65]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2,
                        print_grid=True)

    fig.add_trace(go.Scatter(
        x=labels.index,
        y=labels['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue'),
    ),
        row=1, col=1
    )

    fig.add_trace(go.Scatter(
        x=sell_content.index,
        y=sell_content['preds'].apply(lambda x: values_to_categories.get(x)),
        mode='markers',
        name='Sell',
        hoverinfo='text',
        text=generate_hover_text(sell_content)['hover_text'],
        marker=dict(
            color='red',
            opacity=get_opacities_based_on_confidence(sell_content)
        )
    ),
       row=2, col=1
    )

    fig.add_trace(go.Scatter(
        x=do_nothing_content.index,
        y=do_nothing_content['preds'].apply(lambda x: values_to_categories.get(x)),
        mode='markers',
        name='Do Nothing',
        line=dict(color='lightgrey'),
        hoverinfo='text',
        text=generate_hover_text(do_nothing_content)['hover_text'],
        marker=dict(
            color='lightgrey',
            opacity=get_opacities_based_on_confidence(do_nothing_content)
        )
    ),
        row=2, col=1
    )

    fig.add_trace(go.Scatter(
        x=buy_content.index,
        y=buy_content['preds'].apply(lambda x: values_to_categories.get(x)),
        mode='markers',
        name='Buy',
        line=dict(color='green'),
        hoverinfo='text',
        text=generate_hover_text(buy_content)['hover_text'],
        marker=dict(
            color='green',
            opacity=get_opacities_based_on_confidence(buy_content)
        )
    ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(height=700, width=800, title_text="Buy / Sell Decisions Over Time",
                      showlegend=True,
                      hovermode="x unified")

    # Update x-axis labels
    fig.update_xaxes(title_text="Date", row=2, col=1)

    # Update y-axis labels
    fig.update_yaxes(title_text="Close Price", row=1, col=1)
    fig.update_yaxes(title_text="Sell / Buy", row=2, col=1,
                     categoryorder='array',
                     categoryarray=['Sell', 'Do Nothing', 'Buy'])

    return fig