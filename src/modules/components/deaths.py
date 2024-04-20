import pandas as pd
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px

from ..datasets import main_df
from ..constants import UNIQUE_DRUG_TYPES, COLOR_SEQUENCE
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
    if not selected_drug or not selected_sex:
        return get_px_figure_with_default_template(), "Please select at least one drug type and one sex category"

    start_year, end_year = [pd.to_datetime(x, format='%Y') for x in selected_years]

    # Words to display in the subtitle
    age_display = "All Age Groups" if selected_age == 'Overall' else selected_age
    sex_display = "Both Sexes" if len(selected_sex) == 2 else ''.join(selected_sex)
    title = f"For {sex_display} and {age_display}"

    filtered_df = main_df[(main_df['Drug Type'].isin(selected_drug)) &
                                            main_df['Year'].between(start_year, end_year, inclusive='both') &
                                            main_df['Sex'].isin(selected_sex) &
                                            (main_df['Population Type'] == selected_age)]
    filtered_df = filtered_df.groupby(['Drug Type', 'Year', 'Population Type']).agg({'Deaths': 'sum', 'Death Rate': 'mean'}).reset_index()
    filtered_df = filtered_df.fillna(0)

    fig_deaths_and_rates = px.scatter(
        filtered_df, x='Year',y='Deaths', color='Drug Type',
        size='Death Rate', size_max=45, color_discrete_sequence=COLOR_SEQUENCE,
        hover_data={'Death Rate': ":.1f", "Deaths": ":,"}, category_orders={"Drug Type": UNIQUE_DRUG_TYPES}
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
