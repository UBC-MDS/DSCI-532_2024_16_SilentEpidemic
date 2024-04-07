import pandas as pd
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from .modules.datasets import specific_df, demo_df
from .modules.components import footer, footnote, death_card, death_rate_card, percentage_card, fold_change_card

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'src/assets/styles.css'])
server = app.server


sidebar = html.Div(
    [
        html.H2("National Overdose Deaths Tracker", className="title"),
        html.Hr(),
        html.Div(children=[
            html.H4("Sex"),
            dcc.Dropdown(id='sex_dropdown',
                         options=[
                             {'label': 'All Sexes', 'value': 'All'},
                             {'label': 'Male', 'value': 'Male'},
                             {'label': 'Female', 'value': 'Female'}
                             ],
                             value='All')
                             ]),
        html.Div(children=[
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
        html.Div(children=[
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
        html.Div(children=[
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
def update_demo_figure(selected_drug, selected_years):
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
            orientation="h", yanchor="bottom", y=1.02,
            font=dict(size=8)))

    return fig_demo, title


demo_card = dbc.Card([
    html.H4("Overdose Death Rate based on Demographic", id="demo_title"),
    html.H6("Subtitle", id="demo_subtitle"),
    dcc.Graph(id='demo_graph', figure=fig_demo)
], body=True)


# Create Percentage of Overdoses Involving Opioids per Drug Type Chart
# Create callback for the Percentage of Overdoses Involving Opioids per Drug Type Chart
fig_percent_opioid_deaths = go.Figure()
@app.callback(
    [Output('percent_opioids', 'figure'),
     Output('opioid_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('sex_dropdown', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
     )
def update_opioid_figure(selected_drug, selected_sex, selected_years, selected_age):
    start_year = pd.to_datetime(selected_years[0], format='%Y')
    end_year = pd.to_datetime(selected_years[1], format='%Y')

    # Import dataset and data wrangling for Percentage of Overdoses Involving Opioids per Drug Type plot
    opioid_data_mod = specific_df.copy()
    opioid_data_mod = opioid_data_mod[(opioid_data_mod['Opioid Type'] == 'overall') | (opioid_data_mod['Opioid Type'] == 'any')]
    overall_deaths = opioid_data_mod[opioid_data_mod['Opioid Type'] == 'overall'].groupby(['Drug Type', 'Sex', 'Year', 'Population Type'])['Deaths'].sum()
    opioid_data_mod['Percent Opioid Deaths'] = opioid_data_mod.apply(lambda row: (row['Deaths'] / overall_deaths[(row['Drug Type'], row['Sex'], row['Year'], row['Population Type'])]) * 100 if (row['Drug Type'], row['Sex'], row['Year'], row['Population Type']) in overall_deaths.index else 0, axis=1)
    filtered_opioid_df = opioid_data_mod.query("(`Drug Type` in ['Prescription opioids', 'Synthetic opioids', 'Heroin'] and `Opioid Type` == 'overall') or (`Drug Type` in ['Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'] and `Opioid Type` == 'any')")
    filtered_opioid_df = filtered_opioid_df.dropna(subset=['Percent Opioid Deaths'])
    filtered_opioid_df['Year'] = pd.to_datetime(filtered_opioid_df['Year'], format='%Y')
    
    # Cases to filter the dataset based on inputs
    if selected_age == 'Overall':
        age_display = "All Age Groups"
    else:
        age_display = selected_age

    if selected_sex == 'All':
        sex_display = "Both Sexes"
        sex_categories = ['Male', 'Female']
    else:
        sex_display = selected_sex
        sex_categories = [selected_sex]

    drugs = set(selected_drug.copy())
    drugs_display = set(selected_drug.copy())
    if 'Any opioid' in drugs:
        drugs = list((drugs - {'Any opioid'}) | {'Prescription opioids', 'Synthetic opioids', 'Heroin'})
        drugs_display = list((drugs_display - {'Prescription opioids', 'Synthetic opioids', 'Heroin'}) | {'Any opioid'})

    if set(drugs_display) == {'Any opioid', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'}:
        title = f"All drugs and {sex_display} and {age_display}"
    else:
        title = f"For {' and '.join(drugs_display)} and {sex_display} and {age_display}"

    filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(drugs)) &
                                            filtered_opioid_df['Year'].between(start_year, end_year, inclusive='both') &
                                            filtered_opioid_df['Sex'].isin(sex_categories) &
                                            (filtered_opioid_df['Population Type'] == selected_age)]
    filtered_opioid_df = filtered_opioid_df.groupby(['Drug Type', 'Year', 'Population Type', 'Sex'])['Percent Opioid Deaths'].sum().reset_index()

    
    # Plot Percent Opioid Deaths
    fig_percent_opioid_deaths = px.scatter(filtered_opioid_df, x='Year', y='Percent Opioid Deaths', color='Drug Type', trendline='ols')

    # Update layout
    fig_percent_opioid_deaths.update_layout(
        xaxis_title='Year',
        yaxis_title='Overdoses Involving Opioids (%)',
        legend=dict(orientation="h",yanchor="bottom", y=1.02)
    )
    fig_percent_opioid_deaths.update_yaxes(range=[0, 100])

    return fig_percent_opioid_deaths.to_dict(), title


opioid_card = dbc.Card([
    html.H4("Percentage of Overdoses Involving Opioids by Drug Type", id="opioid_title"),
    html.H6("Subtitle", id="opioid_subtitle"),
    dcc.Graph(id='percent_opioids', figure=fig_percent_opioid_deaths)
], body=True)



fig_deaths_and_rates = go.Figure()

@app.callback(
    [Output('main_graph', 'figure'),
     Output('main_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('sex_dropdown', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
)
def update_main_figure(selected_drug, selected_sex, selected_years, selected_age):
    main_df = specific_df[specific_df['Opioid Type'] == 'overall']
    main_df['Year'] = pd.to_datetime(main_df['Year'], format='%Y')

    start_year = pd.to_datetime(selected_years[0], format='%Y')
    end_year = pd.to_datetime(selected_years[1], format='%Y')

    # Cases to filter the dataset based on inputs
    if selected_age == 'Overall':
        age_display = "All Age Groups"
    else:
        age_display = selected_age

    if selected_sex == 'All':
        sex_display = "Both Sexes"
        sex_categories = ['Male', 'Female']
    else:
        sex_display = selected_sex
        sex_categories = [selected_sex]

    drugs = set(selected_drug.copy())
    drugs_display = set(selected_drug.copy())
    if 'Any opioid' in drugs:
        drugs = list((drugs - {'Any opioid'}) | {'Prescription opioids', 'Synthetic opioids', 'Heroin'})
        drugs_display = list((drugs_display - {'Prescription opioids', 'Synthetic opioids', 'Heroin'}) | {'Any opioid'})

    if set(drugs_display) == {'Any opioid', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines',
                              'Antidepressants'}:
        title = f"All drugs and {sex_display} and {age_display}"
    else:
        title = f"For {' and '.join(drugs_display)} and {sex_display} and {age_display}"

    main_df = main_df[(main_df['Drug Type'].isin(drugs)) &
                                            main_df['Year'].between(start_year, end_year, inclusive='both') &
                                            main_df['Sex'].isin(sex_categories) &
                                            (main_df['Population Type'] == selected_age)]
    filtered_df = main_df.groupby(['Drug Type', 'Year', 'Population Type']).agg({'Deaths': 'sum', 'Death Rate': 'mean'}).reset_index()
    filtered_df = filtered_df.fillna(0)

    fig_deaths_and_rates = px.scatter(filtered_df, x='Year', y='Deaths', color='Drug Type', size='Death Rate', size_max=60)

    # Update layout
    fig_deaths_and_rates.update_layout(xaxis_title='Year', yaxis_title='Deaths',
                                       legend=dict(orientation="h",yanchor="bottom", y=1.02))

    return fig_deaths_and_rates.to_dict(), title


main_card = dbc.Card([
    html.H4("Overdoses Deaths and Death Rates by Drug Type", id="main_title"),
    html.H6("Subtitle", id="main_subtitle"),
    dcc.Graph(id='main_graph', figure=fig_deaths_and_rates)
], body=True)

df_overall = pd.read_csv('data/processed/overall.csv')
@app.callback(
    [Output('death-value', 'children'),
     Output('death-rate-value', 'children'),
     Output('percentage-value', 'children'),
     Output('fold-change-value', 'children')],
    [Input('gender_dropdown', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
     )
def update_aggregated_values(selected_sex, selected_years, selected_age):
    start_year = selected_years[0]
    end_year = selected_years[1]

    filtered_df = df_overall.copy()
    filtered_df = filtered_df[filtered_df['Drug Type'] == "Overall"]

    if selected_sex == 'All':
        sexes = ['Male', 'Female']
    else:
        sexes = [selected_sex]

    filtered_df = filtered_df[filtered_df['Sex'].isin(sexes)]
    filtered_df = filtered_df[filtered_df['Year'].between(start_year, end_year, inclusive='both')]

    pop_df = filtered_df[filtered_df['Population Type'] == selected_age]
    youth_df = filtered_df[filtered_df['Population Type'] == 'Young Adults, 15-24 Years']

    cumulative_deaths = pop_df['Deaths'].sum()

    youth_cumulative_deaths = youth_df['Deaths'].sum()
    young_rate = youth_cumulative_deaths / cumulative_deaths * 100

    group_df = pop_df.groupby(['Year'])
    fold_change = group_df['Deaths'].sum().iloc[-1] / group_df['Deaths'].sum().iloc[0]

    avg_death_rate = (pop_df['Death Rate'] * pop_df['Deaths']).sum() / pop_df['Deaths'].sum()

    formatted_deaths = f"{cumulative_deaths:,.0f}"
    formatted_death_rate = f"{avg_death_rate:.2f}%"
    formatted_percentage_young_adults = f"{young_rate:.2f}%"
    fold_change_text = f"{fold_change:.1f}"

    return formatted_deaths, formatted_death_rate, formatted_percentage_young_adults, fold_change_text


main_dashboard = dbc.Container([
    dbc.Row([
        dbc.Col(death_card, md=3),
        dbc.Col(death_rate_card, md=3),
        dbc.Col(percentage_card, md=3),
        dbc.Col(fold_change_card, md=3),
    ]),
     dbc.Row([
        dbc.Col(main_card, md=12),
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
