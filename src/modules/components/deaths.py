import pandas as pd
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from ..datasets import specific_df


fig_deaths_and_rates = go.Figure()


@callback(
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


deaths_card = dbc.Card([
    html.H4("Overdoses Deaths and Death Rates by Drug Type", id="main_title"),
    html.H6("Subtitle", id="main_subtitle"),
    dcc.Graph(id='main_graph', figure=fig_deaths_and_rates)
], body=True)
