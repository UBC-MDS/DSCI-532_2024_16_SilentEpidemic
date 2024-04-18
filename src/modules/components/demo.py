import plotly.express as px
import plotly.graph_objects as go
from dash import Output, Input, html, dcc, callback
import dash_bootstrap_components as dbc

from ..datasets import demo_df

# create graph for the demographic
fig_demo = go.Figure()


@callback([
    Output('demo_graph', 'figure'),
    Output('demo_subtitle', 'children')
], [
    Input('drug_type_list', 'value'),
    Input('year_range_slider', 'value')
])
def update_demo_figure(selected_drug, selected_years):
    start_year, end_year = selected_years
    filtered_df = demo_df[(demo_df['Year'].between(start_year, end_year))]
    if len(selected_drug) == 8:
        title = "All Drugs"
        filtered_df = filtered_df[(filtered_df['Drug Type'] == 'Total Overdose Deaths')]
    elif len(selected_drug) > 0:
        title = f"For {' and '.join(selected_drug)}"
        filtered_df = filtered_df[(filtered_df['Drug Type'].isin(selected_drug))]
        filtered_df = filtered_df.groupby(['Year', 'Demographic'])['Death Rate'].sum().reset_index()
    else:
        return go.Figure(), "Please select a drug type"

    fig_demo = px.line(filtered_df, x="Year", y="Death Rate", color="Demographic", line_group="Demographic",
        color_discrete_sequence=px.colors.qualitative.T10)

    for trace in fig_demo.data:
        if trace.name == 'Overall':
            trace.line = dict(width=5)
        else:
            trace.opacity = 0.7
        trace.name = trace.name.replace(" (Non-Hispanic)", "")

    fig_demo.update_layout(xaxis_title="Year", yaxis_title="Death Rate <br>(per 100,000 population)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02))

    return fig_demo, title


demo_card = dbc.Card(
    [html.H4("Overdose Death Rate based on Demographic", id="demo_title"), html.H6("Subtitle", id="demo_subtitle"),
        dcc.Graph(id='demo_graph', figure=fig_demo)], body=True)
