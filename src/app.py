from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .modules.components import footer

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

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
            dcc.Dropdown(id='gender_dropdown', 
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
                id='drug_type_list',
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
            html.H2("Filter by Year Range", style={'margin-bottom': '25px'}),
            dcc.RangeSlider(
                id='year_range_slider',
                min=1999, max=2021, step=1,
                value=[1999, 2021],
                marks={1999: "1999", 2004: "2004", 2009: "2009", 
                       2014: "2014", 2019: "2019", 2021: "2021"},
                tooltip={
                    "always_visible": True,
                    "template": "{value}"}
                ),
                ]),    
        html.Div(children=[
            html.H2("Filter by Age Group"),
            dcc.RadioItems(
                id='age_group_radio',
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

test_graph = dcc.Graph(id='example-graph', figure=fig)


# create graph for the demographic
df_demo = pd.read_csv('data/processed/demo.csv')
fig_demo = go.Figure()
@app.callback(
    Output('demo_graph', 'figure'),
    [Input('drug_type_list', 'value'),
     #Input('gender-dropdown', 'value'),
     Input('year_range_slider', 'value')]
     )
def update_figure(selected_drug, selected_years):
    if selected_drug == ['Overall']:
        selected_drug = ['Total Overdose Deaths']
    else:
        selected_drug = selected_drug
    print(selected_drug)
    filtered_df = df_demo[(df_demo['Drug Type'].isin(selected_drug)) &
                          (df_demo['Year'] >= selected_years[0]) &
                          (df_demo['Year'] <= selected_years[1])]
    fig_demo = px.bar(filtered_df, x="Year", y="Death Rate", color="Demographic", barmode="group")
    fig_demo.update_layout(
        title="Overdose Death Rate based on Demographic",
        xaxis_title="Year",
        yaxis_title="Death Rate (per 100,000)",
        legend=dict(
            yanchor="top", y=-0.4,
            xanchor="center", x=0.5,
            font=dict(size=6)))

    return fig_demo


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
        dbc.Col(card, md=6),
        dbc.Col(dcc.Graph(id='demo_graph', figure=fig_demo), md=6)
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
