from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


def create_card(title, value, id_value):
    return dbc.Card(
        [
            html.H4(title, className="card-title", style={"color": "black"}),
            html.H2(value, className="card-value", id=id_value),
        ],
        body=True,
    )


df_overall = pd.read_csv('data/processed/overall.csv')
overall_deaths = df_overall[(df_overall['Drug Type'] == "Overall") &
                            (df_overall['Population Type'] == "Overall")]['Deaths'].sum()

formatted_deaths = f"{overall_deaths:,.0f}"
average_death_rate = df_overall[(df_overall['Drug Type'] == "Overall") &
                            (df_overall['Population Type'] == "Overall")]['Death Rate'].mean()
formatted_death_rate = f"{average_death_rate:.2f}%"
total_deaths_young_adults = df_overall[(df_overall['Drug Type'] == "Overall") &
                                    (df_overall['Population Type'] == "Young Adults, 15-24 Years")]['Deaths'].sum()
percentage_young_adults_deaths = (total_deaths_young_adults / overall_deaths) * 100
formatted_percentage_young_adults = f"{percentage_young_adults_deaths:.2f}%"

overall_deaths_2001 = df_overall[(df_overall['Year'] == 2001) &
                                 (df_overall['Population Type'] == "Overall")]['Deaths'].sum()
overall_deaths_2015 = df_overall[(df_overall['Year'] == 2015) &
                                 (df_overall['Population Type'] == "Overall")]['Deaths'].sum()

# Filter the DataFrame to get the total deaths for Young Adults in 2001 and 2015
young_adults_deaths_2001 = df_overall[(df_overall['Year'] == 2001) &
                                      (df_overall['Population Type'] == "Young Adults, 15-24 Years")]['Deaths'].sum()
young_adults_deaths_2015 = df_overall[(df_overall['Year'] == 2015) &
                                      (df_overall['Population Type'] == "Young Adults, 15-24 Years")]['Deaths'].sum()

# Calculate the fold change for Overall and Young Adults
fold_change_overall = overall_deaths_2015 / overall_deaths_2001
fold_change_young_adults = young_adults_deaths_2015 / young_adults_deaths_2001

# Format the fold change as a string to display in the card
fold_change_text = f"{fold_change_overall:.1f}/{fold_change_young_adults:.1f}"


death_card = create_card("Overall\n", formatted_deaths, "death-value")
death_rate_card = create_card("Death Rate\n", formatted_death_rate, "death-rate-value")
percentage_card = create_card("Percentage of young adults deaths", formatted_percentage_young_adults, "percentage-value")
fold_change_card = create_card("Fold Change (2001-2015)\n(Overall/Young Adults)", fold_change_text, "fold-change-value")

