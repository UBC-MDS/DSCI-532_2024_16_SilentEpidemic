from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
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
            html.H2("Filter by Year Range"),
            dcc.RangeSlider(
                id='year_range_slider',
                min=1999, max=2021, step=1,
                value=[1999, 2021],
                marks={i: str(i) for i in range(1999, 2022, 5)}
                ),
            html.Div(id='display-selected-range')
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

@app.callback(
    Output('display-selected-range', 'children'),
    Input('year_range_slider', 'value')
    )
def update_output(value):
    return 'Years selected: "{}"'.format(value)


test_graph = dcc.Graph(id='example-graph', figure=fig)


# Import dataset and data wrangling for Percentage of Overdoses Involving Opioids per Drug Type plot
opioid_data = pd.read_csv('data/processed/specific.csv')
opioid_data_mod = opioid_data.copy()
opioid_data_mod = opioid_data_mod[(opioid_data_mod['Opioid Type'] == 'overall') | (opioid_data_mod['Opioid Type'] == 'any')]
overall_deaths = opioid_data_mod[opioid_data_mod['Opioid Type'] == 'overall'].groupby(['Drug Type', 'Sex', 'Year', 'Population Type'])['Deaths'].sum()
opioid_data_mod['Percent Opioid Deaths'] = opioid_data_mod.apply(lambda row: (row['Deaths'] / overall_deaths[(row['Drug Type'], row['Sex'], row['Year'], row['Population Type'])]) * 100 if (row['Drug Type'], row['Sex'], row['Year'], row['Population Type']) in overall_deaths.index else 0, axis=1)
filtered_opioid_df = opioid_data_mod.copy().dropna(subset=['Percent Opioid Deaths'])
filtered_opioid_df['Year'] = pd.to_datetime(filtered_opioid_df['Year'], format='%Y')
filtered_opioid_df


# Create callback for the Percentage of Overdoses Involving Opioids per Drug Type Chart
fig_percent_opioid_deaths = go.Figure()
@app.callback(
    Output('percent-opioids', 'figure'),
    [Input('drug_type_list', 'value'),
     Input('gender_dropdown', 'value'),
     Input('year_range_slider', 'value')],
     Input('age_group_radio', 'value')
     )

def update_opioid_figure(selected_drug, selected_gender, selected_years, selected_age):
    # Import dataset and data wrangling for Percentage of Overdoses Involving Opioids per Drug Type plot
    opioid_data = pd.read_csv('data/processed/specific.csv')
    opioid_data_mod = opioid_data.copy()
    opioid_data_mod = opioid_data_mod[(opioid_data_mod['Opioid Type'] == 'overall') | (opioid_data_mod['Opioid Type'] == 'any')]
    overall_deaths = opioid_data_mod[opioid_data_mod['Opioid Type'] == 'overall'].groupby(['Drug Type', 'Sex', 'Year', 'Population Type'])['Deaths'].sum()
    opioid_data_mod['Percent Opioid Deaths'] = opioid_data_mod.apply(lambda row: (row['Deaths'] / overall_deaths[(row['Drug Type'], row['Sex'], row['Year'], row['Population Type'])]) * 100 if (row['Drug Type'], row['Sex'], row['Year'], row['Population Type']) in overall_deaths.index else 0, axis=1)
    filtered_opioid_df = opioid_data_mod.copy().query("(`Drug Type` in ['Prescription opioids', 'Synthetic opioids', 'Heroin'] and `Opioid Type` == 'overall') or (`Drug Type` in ['Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'] and `Opioid Type` == 'any')")
    filtered_opioid_df = filtered_opioid_df.copy().dropna(subset=['Percent Opioid Deaths'])
    filtered_opioid_df['Year'] = pd.to_datetime(filtered_opioid_df['Year'], format='%Y')
    
    # Cases to filter the dataset based on inputs
    if selected_age == 'Overall':
        if selected_gender == 'All':
            if selected_drug == ['Overall']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants']
            elif selected_drug == ['Overall', 'Any opioid']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin']
            else:
                selected_drug = selected_drug

            filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(selected_drug)) &
                                                    (filtered_opioid_df['Year'] >= pd.to_datetime(selected_years[0], format='%Y')) &
                                                    (filtered_opioid_df['Year'] <= pd.to_datetime(selected_years[1], format='%Y'))]
            filtered_opioid_df = filtered_opioid_df.groupby(['Drug Type', 'Year', 'Population Type', 'Sex'])['Percent Opioid Deaths'].sum().reset_index()

        else:
            selected_gender = selected_gender
            print(selected_gender)
            if selected_drug == ['Overall']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants']
            elif selected_drug == ['Overall', 'Any opioid']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin']
            else:
                selected_drug = selected_drug
            filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(selected_drug)) &
                                        (filtered_opioid_df['Year'] >= pd.to_datetime(selected_years[0], format='%Y')) &
                                        (filtered_opioid_df['Year'] <= pd.to_datetime(selected_years[1], format='%Y')) &
                                        (filtered_opioid_df['Sex'] == selected_gender)]
                
    else:
        selected_age == selected_age
        if selected_gender == 'All':
            if selected_drug == ['Overall']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants']
            elif selected_drug == ['Overall', 'Any opioid']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin']
            else:
                selected_drug = selected_drug

            filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(selected_drug)) &
                                                    (filtered_opioid_df['Year'] >= pd.to_datetime(selected_years[0], format='%Y')) &
                                                    (filtered_opioid_df['Year'] <= pd.to_datetime(selected_years[1], format='%Y')) &
                                                    (filtered_opioid_df['Population Type'] == selected_age)]
            filtered_opioid_df = filtered_opioid_df.groupby(['Drug Type', 'Year', 'Population Type', 'Sex'])['Percent Opioid Deaths'].sum().reset_index()

        else:
            selected_gender = selected_gender
            print(selected_gender)
            print(selected_drug)
            if selected_drug == ['Overall']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants']
            elif selected_drug == ['Overall', 'Any opioid']:
                selected_drug = ['Prescription opioids', 'Synthetic opioids', 'Heroin']
            else:
                selected_drug = selected_drug
            filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(selected_drug)) &
                                        (filtered_opioid_df['Year'] >= pd.to_datetime(selected_years[0], format='%Y')) &
                                        (filtered_opioid_df['Year'] <= pd.to_datetime(selected_years[1], format='%Y')) &
                                        (filtered_opioid_df['Sex'] == selected_gender) &
                                        (filtered_opioid_df['Population Type'] == selected_age)]
    
    # Plot Percent Opioid Deaths Plot
    fig_percent_opioid_deaths  = px.scatter(filtered_opioid_df, x='Year', y='Percent Opioid Deaths', color='Drug Type', trendline='ols')

    # Update layout
    fig_percent_opioid_deaths.update_layout(
        xaxis_title='Year',
        yaxis_title='Overdoses Involving Opioids (%)',
    )
    fig_percent_opioid_deaths.update_yaxes(range=[0, 100])

    return fig_percent_opioid_deaths


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
    #print(selected_drug)
    filtered_df = df_demo[(df_demo['Drug Type'].isin(selected_drug)) &
                          (df_demo['Year'] >= selected_years[0]) &
                          (df_demo['Year'] <= selected_years[1])]
    fig_demo = px.bar(filtered_df, x="Year", y="Death Rate", color="Demographic", barmode="group")
    fig_demo.update_layout(
        title="Overdose Death Rate based on Demographic",
        xaxis_title="Year",
        yaxis_title="Death Rate",
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
        dbc.Col(dbc.Card(children=[html.B(children="Percentage of Overdoses Involving Opioids by Drug Type"),dcc.Graph(id='percent-opioids', figure=fig_percent_opioid_deaths)]), md=4),
        dbc.Col(card, md=4),
        dbc.Col(dcc.Graph(id='demo_graph', figure=fig_demo), md=4),
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
