from dash import Dash
import dash_bootstrap_components as dbc

from .modules.components.footnote import footnote
from .modules.components.agg_vals import death_card, death_rate_card, percentage_card, fold_change_card
from .modules.components.demo import demo_card
from .modules.components.opioid import opioid_card
from .modules.components.deaths import deaths_card
from .modules.components.sidebar import sidebar


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'src/assets/styles.css'])
server = app.server

main_dashboard = dbc.Container([
    dbc.Row([
        dbc.Col(death_card, md=3), dbc.Col(death_rate_card, md=3),
        dbc.Col(percentage_card, md=3), dbc.Col(fold_change_card, md=3)
    ]),
    dbc.Row([dbc.Col(deaths_card, md=12)]),
    dbc.Row([dbc.Col(opioid_card, md=6), dbc.Col(demo_card, md=6)]),
    footnote
], fluid=True, className="main-dashboard")


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, md=2),
        dbc.Col(main_dashboard, md=10)
    ])
], fluid=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
