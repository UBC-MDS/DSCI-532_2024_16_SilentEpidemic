from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# test data, to be removed
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#596b7c",
    "color": "#ffffff"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
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
    ],
    style=SIDEBAR_STYLE,
)


main_dashboard = html.Div(children=[
    html.Div(children='Overdose deaths'),

    dcc.Graph(
        id='example-graph',
        figure=fig),
],
    id="page-content",
    style=CONTENT_STYLE)


app.layout = html.Div(children=[
    sidebar, main_dashboard
])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
