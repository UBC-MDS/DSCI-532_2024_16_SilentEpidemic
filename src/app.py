from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from modules.components import footer

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# test data, to be removed
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    "padding": "2rem 1rem",
    "background-color": "#596b7c",
    "color": "#ffffff"
}

PAGE_STYLE = {
}

ROW_STYLE = {
    "margin": "2rem 0rem",
}

CONTENT_STYLE = {
    "margin": "2rem 0",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("National Overdose Deaths Tracker", className="display-4"),
        html.Hr(),
        html.Div(children=[
            html.H2("Filter by Gender"),
            dcc.Dropdown(['All Genders', 'Male', 'Female'], "All Genders", className=""),
        ]),
        html.Div(children=[
            html.H2("Filter by Drug Type"),
            # TODO: checkboxes
        ]),
        html.Div(children=[
            html.H2("Filter by Year Range"),
            # TODO: Double SLider
        ]),
        html.Div(children=[
            # TODO: Toggle button
        ]),
        footer
    ],
    style=SIDEBAR_STYLE,
)

test_graph = dcc.Graph(id='example-graph', figure=fig)

card = dbc.Card(children=[
    html.B(children="Test Graph"),
    test_graph
])

main_dashboard = dbc.Container([
    dbc.Row([
        dbc.Col(card, md=3),
        dbc.Col(card, md=3),
        dbc.Col(card, md=3),
        dbc.Col(card, md=3),
    ], style=ROW_STYLE),
    dbc.Row([
        dbc.Col(card, md=12),
    ], style=ROW_STYLE),
    dbc.Row([
        dbc.Col(card, md=4),
        dbc.Col(card, md=4),
        dbc.Col(card, md=4),
    ], style=ROW_STYLE),
], fluid=True, id="main-dashboard", style=CONTENT_STYLE)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, md=3),
        dbc.Col(main_dashboard, md=9)
    ])
], style=PAGE_STYLE, fluid=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
