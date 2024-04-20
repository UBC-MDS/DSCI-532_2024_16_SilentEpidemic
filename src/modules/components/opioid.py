import pandas as pd
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from ..datasets import specific_df
from ..constants import DRUG_OPIOIDS, unique_drug_types, color_sequence

# Create Percentage of Overdoses Involving Opioids per Drug Type Chart
# Create callback for the Percentage of Overdoses Involving Opioids per Drug Type Chart
fig_percent_opioid_deaths = go.Figure()


@callback(
    [Output('percent_opioids', 'figure'),
     Output('opioid_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('sex_checklist', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
)
def update_opioid_figure(selected_drug, selected_sex, selected_years, selected_age):
    start_year = pd.to_datetime(selected_years[0], format='%Y')
    end_year = pd.to_datetime(selected_years[1], format='%Y')

    # Import dataset and data wrangling for Percentage of Overdoses Involving Opioids per Drug Type plot
    opioid_data_mod = specific_df.copy()
    opioid_data_mod = opioid_data_mod[
        (opioid_data_mod['Opioid Type'] == 'overall') | (opioid_data_mod['Opioid Type'] == 'any')]
    overall_deaths = opioid_data_mod[opioid_data_mod['Opioid Type'] == 'overall'].groupby(
        ['Drug Type', 'Sex', 'Year', 'Population Type'])['Deaths'].sum()
    opioid_data_mod['Percent Opioid Deaths'] = opioid_data_mod.apply(lambda row: (row['Deaths'] / overall_deaths[
        (row['Drug Type'], row['Sex'], row['Year'], row['Population Type'])]) * 100 if (row['Drug Type'], row['Sex'],
                                                                                        row['Year'], row[
                                                                                            'Population Type']) in overall_deaths.index else 0,
                                                                     axis=1)
    filtered_opioid_df = opioid_data_mod.query(
        "(`Drug Type` in ['Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'] and `Opioid Type` == 'any')")
    filtered_opioid_df = filtered_opioid_df.dropna(subset=['Percent Opioid Deaths'])
    filtered_opioid_df['Year'] = pd.to_datetime(filtered_opioid_df['Year'], format='%Y')

    # Cases to filter the dataset based on inputs
    if selected_age == 'Overall':
        age_display = "All Age Groups"
    else:
        age_display = selected_age

    sex_categories = selected_sex
    if len(selected_sex) == 2:
        sex_display = "Both Sexes"
    else:
        sex_display = ''.join(selected_sex)

    drugs = set(selected_drug.copy()) - DRUG_OPIOIDS

    if set(drugs) == {'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'}:
        title = f"All drugs and {sex_display} and {age_display}"
    else:
        title = f"For {' and '.join(drugs)} and {sex_display} and {age_display}"

    filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(drugs)) &
                                            filtered_opioid_df['Year'].between(start_year, end_year, inclusive='both') &
                                            filtered_opioid_df['Sex'].isin(sex_categories) &
                                            (filtered_opioid_df['Population Type'] == selected_age)]
    filtered_opioid_df = filtered_opioid_df.groupby(['Drug Type', 'Year', 'Population Type', 'Sex'])[
        'Percent Opioid Deaths'].sum().reset_index()

    # Create scatter plot with trendlines for males
    fig_percent_opioid_deaths = px.line(
        filtered_opioid_df[filtered_opioid_df['Sex'] == 'Male'], x='Year',
        y='Percent Opioid Deaths', color='Drug Type', color_discrete_sequence=color_sequence,
        category_orders={"Drug Type": unique_drug_types} 
    )
    for trace in fig_percent_opioid_deaths.data:
        trace.line.dash = 'dash'
        trace.name += ' (Male)' 

    # Add scatter points for females to the existing plot
    for trace in px.line(
            filtered_opioid_df[filtered_opioid_df['Sex'] == 'Female'], x='Year',
            y='Percent Opioid Deaths', color='Drug Type', color_discrete_sequence=color_sequence,
            category_orders={"Drug Type": unique_drug_types} 
    ).data:
        trace.name += ' (Female)' 
        fig_percent_opioid_deaths.add_trace(trace)

    # Update layout
    fig_percent_opioid_deaths.update_layout(
        xaxis_title='Year',
        yaxis_title='Overdoses Involving Opioids (%)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig_percent_opioid_deaths.update_yaxes(range=[0, 100])

    return fig_percent_opioid_deaths.to_dict(), title


opioid_card = dbc.Card([
    html.H4("Percentage of Overdose Deaths Involving Opioids as a Secondary Factor", id="opioid_title"),
    html.H6("Subtitle", id="opioid_subtitle"),
    dcc.Graph(id='percent_opioids', figure=fig_percent_opioid_deaths)
], body=True)
