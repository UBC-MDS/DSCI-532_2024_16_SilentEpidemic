from datetime import datetime

import requests
import plotly.graph_objects as go

from .constants import API_ENDPOINT


def get_repo_last_updated_time():
    repo_info = requests.get(API_ENDPOINT).json()
    return datetime.fromisoformat(repo_info['pushed_at'])


def get_px_figure_with_default_template():
    return go.Figure(layout=dict(template='plotly'))


def get_placeholder_figure(message="Nothing to show.", fontsize=16):
    fig = get_px_figure_with_default_template()
    fig.add_annotation(
        x=5,
        y=5,
        text=message,
        font={'family': "system-ui", 'size': fontsize},
        showarrow=False
    ).update_yaxes(range=[0, 10]).update_xaxes(range=[0, 10])
    return fig
