from dash import html
import dash_bootstrap_components as dbc


def create_card(title, value, id_value):
    return dbc.Card(
        [
            html.H4(title, className="card-title", style={"color": "black"}),
            html.H2(value, className="card-value", id=id_value),
        ],
        body=True,
    )


death_card = create_card("Cumulative Deaths from All Drugs", 0, "death-value")
death_rate_card = create_card("Average Death Rate", 0, "death-rate-value")
percentage_card = create_card("Percentage of Young Adults deaths", 0, "percentage-value")
fold_change_card = create_card("Fold Change", 0, "fold-change-value")

