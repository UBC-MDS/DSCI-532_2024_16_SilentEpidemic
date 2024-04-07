from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from .modules.datasets import specific_df, demo_df
from .modules.components import footer, footnote, death_card, death_rate_card, percentage_card, fold_change_card

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'src/assets/styles.css'])
server = app.server


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
                    value=['Any opioid', 'Prescription opioids', 'Synthetic opioids', 'Heroin', 
                           'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'])
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
    ], className="sidebar"
)


# create graph for the demographic
fig_demo = go.Figure()
@app.callback(
    [Output('demo_graph', 'figure'),
    Output('demo_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('year_range_slider', 'value')]
)
def update_figure(selected_drug, selected_years):
    print(selected_drug)
    if len(selected_drug) == 9:
        selected_drug = ['Total Overdose Deaths']
        title = "All Drugs"
    else:
        selected_drug = selected_drug
        title = f"For {' and '.join(selected_drug)}"
    filtered_df = demo_df[(demo_df['Drug Type'].isin(selected_drug)) &
                          (demo_df['Year'] >= selected_years[0]) &
                          (demo_df['Year'] <= selected_years[1])]
    fig_demo = px.bar(filtered_df, x="Year", y="Death Rate", color="Demographic", barmode="group")
    
    fig_demo.update_layout(
        xaxis_title="Year",
        yaxis_title="Death Rate <br>(per 100,000 population)",
        legend=dict(
            x=0, y=-0.2,
            xanchor='center', yanchor='top',
            orientation='h',
            font=dict(size=8)))

    return fig_demo, title


demo_card = dbc.Card([
    html.H4("Overdose Death Rate based on Demographic", id="demo_title"),
    html.H6("Subtitle", id="demo_subtitle"),
    dcc.Graph(id='demo_graph', figure=fig_demo)
])

main_dashboard = dbc.Container([
    dbc.Row([
        dbc.Col(death_card, md=3),
        dbc.Col(death_rate_card, md=3),
        dbc.Col(percentage_card, md=3),
        dbc.Col(fold_change_card, md=3),
    ]),
     dbc.Row([
        dbc.Col(demo_card, md=12),
    ]),
    dbc.Row([
        dbc.Col(demo_card, md=6),
        dbc.Col(demo_card, md=6),
    ]),
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
