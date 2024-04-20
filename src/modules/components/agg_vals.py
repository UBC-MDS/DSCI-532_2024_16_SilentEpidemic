from dash import html, Output, Input, callback
import dash_bootstrap_components as dbc

from ..datasets import overall_df


def create_card(title, value, id_value):
    return dbc.Card(
        [
            html.H4(title, className="card-title"),
            html.P(value, className="card-value", id=id_value),
        ],
        body=True,
    )


@callback(
    [Output('death_value', 'children'),
     Output('death_rate_value', 'children'),
     Output('percentage_value', 'children'),
     Output('fold_change_value', 'children')],
    [Input('sex_checklist', 'value'),
     Input('year_range_slider', 'value'),
     Input('age_group_radio', 'value')]
     )
def update_aggregated_values(selected_sex, selected_years, selected_age):
    start_year = selected_years[0]
    end_year = selected_years[1]

    filtered_df = overall_df.copy()
    filtered_df = filtered_df[filtered_df['Drug Type'] == "Overall"]

    filtered_df = filtered_df[filtered_df['Sex'].isin(selected_sex)]
    filtered_df = filtered_df[filtered_df['Year'].between(start_year, end_year, inclusive='both')]

    pop_df = filtered_df[filtered_df['Population Type'] == selected_age]
    youth_df = filtered_df[filtered_df['Population Type'] == 'Young Adults, 15-24 Years']

    cumulative_deaths = pop_df['Deaths'].sum()

    youth_cumulative_deaths = youth_df['Deaths'].sum()
    young_rate = youth_cumulative_deaths / cumulative_deaths * 100

    group_df = pop_df.groupby(['Year'])
    fold_change = group_df['Deaths'].sum().iloc[-1] / group_df['Deaths'].sum().iloc[0]

    avg_death_rate = group_df['Death Rate'].mean().mean()

    formatted_deaths = f"{cumulative_deaths:,.0f}"
    formatted_death_rate = f"{avg_death_rate:.2f}"
    formatted_percentage_young_adults = f"{young_rate:.2f}%"
    fold_change_text = f"{fold_change:.1f}"

    return formatted_deaths, formatted_death_rate, formatted_percentage_young_adults, fold_change_text


death_card = create_card("Cumulative Deaths from All Drugs", 0, "death_value")
death_rate_card = create_card("Average Death Rate (All Drugs, per 100,000)", 0, "death_rate_value")
percentage_card = create_card("Percentage Young Adult Deaths", 0, "percentage_value")
fold_change_card = create_card("Fold Change", 0, "fold_change_value")
