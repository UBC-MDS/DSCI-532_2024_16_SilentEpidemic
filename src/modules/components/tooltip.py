from dash import html
import dash_bootstrap_components as dbc


def create_tooltip(tooltip_id, message):
    return html.Span([
        html.Span(id=tooltip_id, className="bi bi-info-circle-fill px-2 fs-6"),
        dbc.Tooltip(message, target=tooltip_id, placement="top"),
    ], className="tooltip-wrapper")