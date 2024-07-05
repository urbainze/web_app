import dash_bootstrap_components as dbc
from dash import html,Dash,dcc





# Define the layout
cards = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
            ),
            style={"height": "500px", "margin-left": "2rem", "margin-right": "2rem", "background-color": "white"}
        )
    ]
)

monitoring_layout = html.Div(children = [html.Br(),cards])