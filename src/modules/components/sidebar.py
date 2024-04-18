from dash import html, dcc
import dash_bootstrap_components as dbc

from .footer import footer


sidebar = dbc.Container([
    dbc.Col([
        dbc.Row([
            html.H2("National Overdose Deaths Tracker", className="title"),
        ]),
        dbc.Row([html.Hr()]),
        dbc.Row([
            html.H4("Drug Type"),
            dcc.Dropdown(
                id='drug_type_list',
                options=[
                    {'label': 'Prescription opioids', 'value': 'Prescription opioids'},
                    {'label': 'Synthetic opioids', 'value': 'Synthetic opioids'},
                    {'label': 'Heroin (opioids)', 'value': 'Heroin'},
                    {'label': 'Stimulants', 'value': 'Stimulants'},
                    {'label': 'Cocaine', 'value': 'Cocaine'},
                    {'label': 'Psychostimulants', 'value': 'Psychostimulants'},
                    {'label': 'Benzodiazepines', 'value': 'Benzodiazepines'},
                    {'label': 'Antidepressants', 'value': 'Antidepressants'},
                ],
                value=['Prescription opioids', 'Synthetic opioids', 'Heroin',
                       'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'],
                placeholder = "Select a drug type",
                multi=True)
                       
        ]),
        dbc.Row([html.Hr()]),
        dbc.Row([
            html.H4("Year Range", style={'margin-bottom': '25px'}),
            dcc.RangeSlider(
                id='year_range_slider',
                min=1999, max=2021, step=1,
                value=[1999, 2021],
                marks={1999: "1999", 2004: "2004", 2009: "2009",
                       2014: "2014", 2019: "2019", 2021: "2021"},
                tooltip={
                    "placement": "bottom",
                    "always_visible": True,
                    "template": "{value}"}
            ),
        ]),
        dbc.Row([html.Hr()]),
        dbc.Row([
            html.H4("Sex"),
            dcc.Checklist(id='sex_checklist', options=['Male', 'Female'], value=['Male', 'Female'])
        ]),
        dbc.Row([html.Hr()]),
        dbc.Row([
            html.H4("Age Group"),
            dcc.RadioItems(
                id='age_group_radio',
                options=[
                    {'label': 'Young Adults, 15-24 Years', 'value': 'Young Adults, 15-24 Years'},
                    {'label': 'Overall', 'value': 'Overall'}
                ],
                value='Overall'  # Default selected value
            )
        ]),
        dbc.Row([html.Hr()]),
        dbc.Row([html.A(
            dbc.Button(
                "Reset All Filters",color="light",
                className="me-1 link-underline-opacity-0", outline=True),
            href='/', className="d-grid gap-2 link-underline-opacity-0")]),
        dbc.Row([footer])
    ])
], className="sidebar", fluid=True)
