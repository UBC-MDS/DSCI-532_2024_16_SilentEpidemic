from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import plotly.express as px
import pandas as pd
from modules.components import footer


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

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

def create_card(title, value, id_value):
    return dbc.Card(
        [
            html.H4(title, className="card-title", style={"color": "black"}),
            html.H2(value, className="card-value", id=id_value),
        ],
        body=True,
        style={"textAlign": "center", "color": "red"}
    )


death_card = create_card("Overall\n", formatted_deaths, "death-value")
death_rate_card = create_card("Death Rate\n", formatted_death_rate, "death-rate-value")
percentage_card = create_card("Percentage of young adults deaths", formatted_percentage_young_adults, "percentage-value")
fold_change_card = create_card("Fold Change (2001-2015)\n(Overall/Young Adults)", fold_change_text, "fold-change-value")

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
    'display': 'flex',
    'flex-wrap': 'wrap',  # Allow the items to wrap on smaller screens
    'align-items': 'stretch'
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
            dcc.Dropdown(['All Genders', 'Male', 'Female'], "All Genders", className=""),
        ]),
        html.Div(children=[
            html.H2("Filter by Drug Type"),
            # TODO: checkboxes
        ]),
        html.Div(children=[
            html.H2("Filter by Year Range"),
            # TODO: Double SLider
        ]),
        html.Div(children=[
            # TODO: Toggle button
        ]),
        footer
    ],
    style=SIDEBAR_STYLE,
)


CARD_STYLE = {
    "height": "50px",  
    "margin-bottom": "10px"  
    
}

main_dashboard = dbc.Container([
    dbc.Row([
        dbc.Col(death_card, style=CARD_STYLE, md=3),
        dbc.Col(death_rate_card, style=CARD_STYLE, md=3),
        dbc.Col(percentage_card, style=CARD_STYLE, md=3),
        dbc.Col(fold_change_card, style=CARD_STYLE, md=3),
    ], style=ROW_STYLE),
     dbc.Row([
        # dbc.Col(card, md=12),
    ], style=ROW_STYLE),
    dbc.Row([
        """ dbc.Col(card, md=4),
        dbc.Col(card, md=4),
        dbc.Col(card, md=4),  """
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
