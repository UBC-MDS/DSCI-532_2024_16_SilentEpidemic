from dash import html, dcc
import dash_bootstrap_components as dbc

from .footer import footer

sidebar = dbc.Container([
    dbc.Col([
        dbc.Row([
            html.H2("National Overdose Deaths Tracker", className="title"),
        ]),
        dbc.Row([
            html.Hr(),
        ]),
        dbc.Row([
            html.H4("Sex"),
            dcc.Dropdown(id='sex_dropdown',
                         options=[
                             {'label': 'All Sexes', 'value': 'All'},
                             {'label': 'Male', 'value': 'Male'},
                             {'label': 'Female', 'value': 'Female'}
                         ],
                         value='All')
        ]),
        dbc.Row([
            html.H4("Drug Type"),
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
                value=['Any opioid', 'Prescription opioids', 'Synthetic opioids', 'Heroin',
                       'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'])
        ]),
        dbc.Row([
            html.H4("Year Range", style={'margin-bottom': '25px'}),
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
        dbc.Row([footer])
    ])
], className="sidebar", fluid=True
)
