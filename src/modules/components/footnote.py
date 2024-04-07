from dash import html
import dash_bootstrap_components as dbc


footnote = dbc.Row([
    html.P("Note: There may be instances of double counting in the data. For example, \
       a death involving both heroin and opioid would be counted in both the heroin and opioid\
       categories.")], className="footnote")