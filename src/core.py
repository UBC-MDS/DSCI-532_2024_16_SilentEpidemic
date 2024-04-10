from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'src/assets/styles.css'])
server = app.server