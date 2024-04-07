from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules.components import footer, footnote, death_card, death_rate_card, percentage_card, fold_change_card

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
                             {'label': 'All Sexes', 'value': 'All'},
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
df_demo = pd.read_csv('data/processed/demo.csv')
fig_demo = go.Figure()
@app.callback(
    [Output('demo_graph', 'figure'),
    Output('demo_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('year_range_slider', 'value')]
)
def update_figure(selected_drug, selected_years):
    if len(selected_drug) == 9:
        selected_drug = ['Total Overdose Deaths']
        title = "All Drugs"
    else:
        selected_drug = selected_drug
        title = f"For {' and '.join(selected_drug)}"
    filtered_df = df_demo[(df_demo['Drug Type'].isin(selected_drug)) &
                          (df_demo['Year'] >= selected_years[0]) &
                          (df_demo['Year'] <= selected_years[1])]
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

opioid_data = pd.read_csv('data/processed/specific.csv')


# Create Percentage of Overdoses Involving Opioids per Drug Type Chart
# Create callback for the Percentage of Overdoses Involving Opioids per Drug Type Chart
fig_percent_opioid_deaths = go.Figure()
@app.callback(
    [Output('percent_opioids', 'figure'),
     Output('opioid_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('gender_dropdown', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
     )
def update_opioid_figure(selected_drug, selected_gender, selected_years, selected_age):
    start_year = pd.to_datetime(selected_years[0], format='%Y')
    end_year = pd.to_datetime(selected_years[1], format='%Y')

    # Import dataset and data wrangling for Percentage of Overdoses Involving Opioids per Drug Type plot
    opioid_data_mod = opioid_data.copy()
    opioid_data_mod = opioid_data_mod[(opioid_data_mod['Opioid Type'] == 'overall') | (opioid_data_mod['Opioid Type'] == 'any')]
    overall_deaths = opioid_data_mod[opioid_data_mod['Opioid Type'] == 'overall'].groupby(['Drug Type', 'Sex', 'Year', 'Population Type'])['Deaths'].sum()
    opioid_data_mod['Percent Opioid Deaths'] = opioid_data_mod.apply(lambda row: (row['Deaths'] / overall_deaths[(row['Drug Type'], row['Sex'], row['Year'], row['Population Type'])]) * 100 if (row['Drug Type'], row['Sex'], row['Year'], row['Population Type']) in overall_deaths.index else 0, axis=1)
    filtered_opioid_df = opioid_data_mod.copy().query("(`Drug Type` in ['Prescription opioids', 'Synthetic opioids', 'Heroin'] and `Opioid Type` == 'overall') or (`Drug Type` in ['Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'] and `Opioid Type` == 'any')")
    filtered_opioid_df = filtered_opioid_df.copy().dropna(subset=['Percent Opioid Deaths'])
    filtered_opioid_df['Year'] = pd.to_datetime(filtered_opioid_df['Year'], format='%Y')
    
    # Cases to filter the dataset based on inputs
    if selected_age == 'Overall':
        age_display = "All Age Groups"
    else:
        age_display = selected_age

    if selected_gender == 'All':
        gender_display = "Both Sexes"
        gender_categories = ['Male', 'Female']
    else:
        gender_display = selected_gender
        gender_categories = [selected_gender]

    if selected_drug == ['Any opioid', 'Prescription opioids', 'Synthetic opioids', 'Heroin', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants']:
        selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants']
        title = f"All drugs and {gender_display} and {age_display}"
    elif selected_drug == ['Any opioid']:
        selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin']
        title = f"For Any Opioid and {gender_display} and {age_display}"
    else:
        title = f"For {' and '.join(selected_drug)} and {gender_display} and {age_display}"

    filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(selected_drug)) &
                                            filtered_opioid_df['Year'].between(start_year, end_year, inclusive='both') &
                                            filtered_opioid_df['Sex'].isin(gender_categories) &
                                            (filtered_opioid_df['Population Type'] == selected_age)]
    filtered_opioid_df = filtered_opioid_df.groupby(['Drug Type', 'Year', 'Population Type', 'Sex'])['Percent Opioid Deaths'].sum().reset_index()

    
    # Plot Percent Opioid Deaths
    fig_percent_opioid_deaths = px.scatter(filtered_opioid_df, x='Year', y='Percent Opioid Deaths', color='Drug Type', trendline='ols')

    # Update layout
    fig_percent_opioid_deaths.update_layout(
        xaxis_title='Year',
        yaxis_title='Overdoses Involving Opioids (%)',
    )
    fig_percent_opioid_deaths.update_yaxes(range=[0, 100])

    return fig_percent_opioid_deaths.to_dict(), title


opioid_card = dbc.Card([
    html.H4("Percentage of Overdoses Involving Opioids by Drug Type", id="opioid_title"),
    html.H6("Subtitle", id="opioid_subtitle"),
    dcc.Graph(id='percent_opioids', figure=fig_percent_opioid_deaths)
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
        dbc.Col(opioid_card, md=6),
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
