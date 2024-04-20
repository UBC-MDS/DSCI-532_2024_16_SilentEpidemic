from datetime import datetime

import requests
import plotly.graph_objects as go

from .constants import API_ENDPOINT


def get_repo_last_updated_time():
    repo_info = requests.get(API_ENDPOINT).json()
    return datetime.fromisoformat(repo_info['pushed_at'])


def get_px_figure_with_default_template():
    return go.Figure(layout=dict(template='plotly'))
