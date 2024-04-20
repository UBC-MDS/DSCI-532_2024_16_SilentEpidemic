import pandas as pd
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px

from ..datasets import specific_df
from ..constants import DRUG_OPIOIDS
from ..utils import get_px_figure_with_default_template


fig_deaths_and_rates = get_px_figure_with_default_template()


@callback(
    [Output('main_graph', 'figure'),
     Output('main_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('sex_checklist', 'value'),
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

    sex_categories = selected_sex
    if len(selected_sex) == 2:
        sex_display = "Both Sexes"
    else:
        sex_display = ''.join(selected_sex)

    drugs_display = set(selected_drug.copy())
    if DRUG_OPIOIDS.issubset(drugs_display):
        drugs_display = list((drugs_display - DRUG_OPIOIDS) | {'Any opioid'})

    if set(drugs_display) == {'Any opioid', 'Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines',
                              'Antidepressants'}:
        title = f"All drugs and {sex_display} and {age_display}"
    else:
        title = f"For {' and '.join(drugs_display)} and {sex_display} and {age_display}"

    main_df = main_df[(main_df['Drug Type'].isin(selected_drug)) &
                                            main_df['Year'].between(start_year, end_year, inclusive='both') &
                                            main_df['Sex'].isin(sex_categories) &
                                            (main_df['Population Type'] == selected_age)]
    filtered_df = main_df.groupby(['Drug Type', 'Year', 'Population Type']).agg({'Deaths': 'sum', 'Death Rate': 'mean'}).reset_index()
    filtered_df = filtered_df.fillna(0)

    fig_deaths_and_rates = px.scatter(
        filtered_df, x='Year',y='Deaths', color='Drug Type',
        size='Death Rate', size_max=45, color_discrete_sequence=px.colors.qualitative.Prism,
        hover_data={'Death Rate': ":.2f", "Deaths": ":,"}
    )

    # Update layout
    fig_deaths_and_rates.update_layout(xaxis_title='Year', yaxis_title='Deaths',
                                       legend=dict(orientation="h", yanchor="bottom", y=1.02))

    # Add hints indicating bubble size as death rate
    # This is added since plotly currently does not support displaying a legend for marker size
    # Possible workaround exists but requires creating another trace which is not ideal for the styling
    #
    # Refer to:
    # https://github.com/plotly/plotly.py/issues/3505
    # https://github.com/plotly/plotly.js/issues/5099
    # https://stackoverflow.com/questions/66190742/plotly-scatter-bubble-plot-marker-size-in-legend?noredirect=1&lq=1
    # https://stackoverflow.com/questions/66686072/size-legend-for-plotly-express-scatterplot-in-python

    title = title + ", Death Rate Proportional to Size of Bubbles"

    return fig_deaths_and_rates.to_dict(), title


deaths_card = dbc.Card([
    html.H4("Overdoses Deaths and Death Rates by Drug Type", id="main_title"),
    html.H6("Subtitle", id="main_subtitle"),
    dcc.Graph(id='main_graph', figure=fig_deaths_and_rates)
], body=True)
