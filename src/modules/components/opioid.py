import pandas as pd
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px

from ..datasets import opioid_df
from ..constants import DRUG_OPIOIDS, UNIQUE_DRUG_TYPES, COLOR_SEQUENCE
from ..utils import get_px_figure_with_default_template


fig_percent_opioid_deaths = get_px_figure_with_default_template()


@callback(
    [Output('percent_opioids', 'figure'),
     Output('opioid_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('sex_checklist', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
)
def update_opioid_figure(selected_drug, selected_sex, selected_years, selected_age):
    if not selected_drug or not selected_sex:
        return get_px_figure_with_default_template(), "Please select at least one drug type and one sex category"
     
    start_year, end_year = [pd.to_datetime(x, format='%Y') for x in selected_years]

    filtered_opioid_df = opioid_df.dropna(subset=['Percent Opioid Deaths'])

    # Words to display in the subtitle
    age_display = "All Age Groups" if selected_age == 'Overall' else selected_age
    sex_display = "Both Sexes" if len(selected_sex) == 2 else ''.join(selected_sex)
    title = f"For {sex_display} and {age_display}"

    drugs = set(selected_drug.copy()) - DRUG_OPIOIDS

    filtered_opioid_df = filtered_opioid_df[(filtered_opioid_df['Drug Type'].isin(drugs)) &
                                            filtered_opioid_df['Year'].between(start_year, end_year, inclusive='both') &
                                            filtered_opioid_df['Sex'].isin(selected_sex) &
                                            (filtered_opioid_df['Population Type'] == selected_age)]

    # Create scatter plot with trendlines for males
    fig_percent_opioid_deaths = px.line(
        filtered_opioid_df[filtered_opioid_df['Sex'] == 'Male'], x='Year',
        y='Percent Opioid Deaths', color='Drug Type', color_discrete_sequence=COLOR_SEQUENCE,
        category_orders={"Drug Type": UNIQUE_DRUG_TYPES}, hover_data = {'Percent Opioid Deaths': ":.1f"}
    )
    for trace in fig_percent_opioid_deaths.data:
        trace.line.dash = 'dash'
        trace.name += ' (Male)' 

    # Add scatter points for females to the existing plot
    for trace in px.line(
            filtered_opioid_df[filtered_opioid_df['Sex'] == 'Female'], x='Year',
            y='Percent Opioid Deaths', color='Drug Type', color_discrete_sequence=COLOR_SEQUENCE,
            category_orders={"Drug Type": UNIQUE_DRUG_TYPES}, hover_data = {'Percent Opioid Deaths': ":.1f"}
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
