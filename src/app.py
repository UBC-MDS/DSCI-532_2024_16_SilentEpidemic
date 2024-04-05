from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# test data, to be removed
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# 3rd plot: create plot related to fentanyl
df_rate = pd.read_csv('data/processed/od_deathrate.csv', index_col=0)
df_rate = df_rate[:-2]
df_plot3 = df_rate[['Synthetic Opioids other than Methadone (primarily fentanyl)3',
                   'Synthetic Opioids other than Methadone (primarily fentanyl)3 Female',
                   'Synthetic Opioids other than Methadone (primarily fentanyl)3 Male']]
categories = df_plot3.index 
fen_fig = go.Figure()

@app.callback(
    Output('fen-graph', 'figure'),  # id of your graph component
    [Input('gender-dropdown', 'value')]
)
def update_figure(selected_gender):
    # Filter your DataFrame based on the selected gender
    if selected_gender == 'All':
        df_filtered = df_plot3
    elif selected_gender == 'Male':
        df_filtered = df_plot3[['Synthetic Opioids other than Methadone (primarily fentanyl)3 Male']]
    elif selected_gender == 'Female':
        df_filtered = df_plot3[['Synthetic Opioids other than Methadone (primarily fentanyl)3 Female']]
    else:
        df_filtered = df_plot3

    # Create a trace for each dataset
    traces = []
    for col in df_filtered.columns:
        traces.append(go.Scatter(x=df_filtered.index, y=df_filtered[col], mode='lines', name=selected_gender))

    # Create the data and layout objects
    layout = go.Layout(title=f'Death Rate Related to Fentanyl for {selected_gender}',
                       yaxis=dict(title='Death Rate'),
                       xaxis=dict(title='Year'),
                       legend=dict(yanchor="top", y=-0.4, 
                                   xanchor="center", x=0.5,
                                   font=dict(size=8))) 

    # Create the figure and add the data and layout
    fen_fig = go.Figure(data=traces, layout=layout)

    return fen_fig


# 4th plot: create plot for the demographic
df_demo = pd.read_csv('data/processed/od_rate_demo.csv', index_col=0)
df_demo = df_demo[:-1]
categories = df_demo.index
trace1 = go.Bar(x=categories, y=df_demo['total White (Non-Hispanic)'], name='Total White')
trace2 = go.Bar(x=categories, y=df_demo['total Black (Non-Hispanic)'], name='Total Black')
trace3 = go.Bar(x=categories, y=df_demo['total Asian* (Non-Hispanic)'], name='Total Asian')
trace4 = go.Bar(x=categories, y=df_demo['total Native Hawaiin or Other Pacific Islander* (Non-Hispanic)'], name='Total Native Hawaiin or Other Pacific Islander')
trace5 = go.Bar(x=categories, y=df_demo['total Hispanic'], name='Total Hispanic')
trace6 = go.Bar(x=categories, y=df_demo['total American Indian or Alaska Native (Non-Hispanic)'], name='Total American Indian or Alaska Native')
data = [trace1, trace2, trace3, trace4, trace5, trace6]
layout = go.Layout(title= "Overdose Death Rate based on Demographic",
                   yaxis=dict(title='Death Rate'),
                   xaxis= dict(title= 'Year'),
                   legend=dict(yanchor="top", y=-0.4, 
                               xanchor="center", x=0.5,
                               font=dict(size=8)),
                   barmode='group')
demo_fig = go.Figure(data=data, layout=layout)



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#596b7c",
    "color": "#ffffff"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
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
    ],
    style=SIDEBAR_STYLE,
)


main_dashboard = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(children='Overdose deaths')),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='example-graph', figure=fig)),
    ]),
    dbc.Row([
        #testing of filter gender to be removed later
        dbc.Col(dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'All Genders', 'value': 'All'},
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ],
        value='All')),
        dbc.Col(dcc.Graph(id='fen-graph', figure=fen_fig)),
        dbc.Col(dcc.Graph(id='demo-graph', figure=demo_fig))
    ])
],
    id="page-content",
    style=CONTENT_STYLE)


app.layout = html.Div(children=[
    sidebar, main_dashboard
])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
