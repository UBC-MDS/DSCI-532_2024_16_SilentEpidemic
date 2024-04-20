from dash import html, dcc

from ..constants import REPO_URL
from ..utils import get_repo_last_updated_time


footer = html.Footer(children=[
    html.Div("This is a dashboard for visualizing the trend in deaths caused by drug overdoses in the United States from 1999 to 2021."),
    html.Br(),
    html.Div("Authors: Orix Au Yeung (@SoloSynth1), Yingzi Jin (@jinyz8888), Alysen Townsley (@AlysenTownsley), Bill Wan (@billwan96)"),
    html.Br(),
    dcc.Link(children="Link to repo", href=REPO_URL, target="_blank"),
    html.Br(),
    html.Div("Last Updated: " + get_repo_last_updated_time().strftime("%B %d, %Y")),
], className="footer")