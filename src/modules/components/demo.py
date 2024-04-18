import plotly.express as px
import plotly.graph_objects as go
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc

from ..datasets import demo_df


# create graph for the demographic
fig_demo = go.Figure()


@callback(
    [Output('demo_graph', 'figure'),
     Output('demo_subtitle', 'children')],
    [Input('drug_type_list', 'value'),
     Input('year_range_slider', 'value')]
)
def update_demo_figure(selected_drug, selected_years):
    if len(selected_drug) == 8:
        title = "All Drugs"
    else:
        title = f"For {' and '.join(selected_drug)}"
    filtered_df = demo_df[(demo_df['Drug Type'].isin(selected_drug)) &
                          (demo_df['Year'] >= selected_years[0]) &
                          (demo_df['Year'] <= selected_years[1])]
    fig_demo = px.bar(
        filtered_df, x="Year", y="Death Rate", color="Demographic",
        barmode="group", color_discrete_sequence=px.colors.qualitative.T10)

    fig_demo.update_layout(
        xaxis_title="Year",
        yaxis_title="Death Rate <br>(per 100,000 population)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            font=dict(size=8)))

    return fig_demo, title


demo_card = dbc.Card([
    dbc.Alert(
        [
            html.H4(id="demo_title", children="Overdose Death Rate based on Demographic "),
            html.I(id="info_icon", className="bi bi-info-circle-fill me-2"),
        ],
        id="infotitle_box",
        className="d-flex align-items-center",
    ),
    html.H6("Subtitle", id="demo_subtitle"),
    dbc.Tooltip(
        "This chart shows the overdose death rate based on demographic only for both sexes and overall agegroup.",
        target="info_icon",
        placement="right"
    ),
    dcc.Graph(id='demo_graph', figure=fig_demo)
], body=True)
