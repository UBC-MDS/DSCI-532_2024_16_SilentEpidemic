from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
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
            dcc.Dropdown(id='gender-dropdown', 
                         options=[
                             {'label': 'All Genders', 'value': 'All'},
                             {'label': 'Male', 'value': 'Male'},
                             {'label': 'Female', 'value': 'Female'}
                             ],
                             value='All')
                             ]),
        html.Div(children=[
            html.H2("Filter by Drug Type"),
            dcc.Checklist(
                id='drug_type',
                options=[
                    {'label': 'Any opioid', 'value': 'Any opioid'},
                    {'label': 'Prescription opioids', 'value': 'Prescription opioids'},
                    {'label': 'Synthetic opioids', 'value': 'Synthetic opioids'},
                    {'label': 'Heroin', 'value': 'Heroin'},
                    {'label': 'Stimulants', 'value': 'Stimulants'},
                    {'label': 'Cocaine', 'value': 'Cocaine'},
                    {'label': 'Psychostimulants', 'value': 'Psychostimulants'},
                    {'label': 'Benzodiazepines', 'value': 'Benzodiazepines'},
                    {'label': 'Antidepressants', 'value': 'Antidepressants'},        
                    ],
                    value=['Overall']  # Default selected value
                    )
                    ]),
        html.Div(children=[
            html.H2("Filter by Year Range"),
            dcc.RangeSlider(
                id='year_range',
                min=1999, max=2021, step=1,
                value=[1999, 2021],
                marks={i: str(i) for i in range(1999, 2022, 5)}
                ),
            html.Div(id='display-selected-range')
                ]),
                
        html.Div(children=[
            html.H2("Filter by Age Group"),
            dcc.RadioItems(
                id='age_group',
                options=[
                    {'label': 'Young Adults, 15-24 Years', 'value': 'Young Adults, 15-24 Years'},
                    {'label': 'Overall', 'value': 'Overall'}
                    ],
                    value='Overall'  # Default selected value
                    )
                    ]),
        footer
    ],
    style=SIDEBAR_STYLE,
)

@app.callback(
    Output('display-selected-range', 'children'),
    Input('year_range', 'value')
)
def update_output(value):
    return 'Years selected: "{}"'.format(value)

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
