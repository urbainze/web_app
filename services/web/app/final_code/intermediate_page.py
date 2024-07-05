import dash_bootstrap_components as dbc
from dash import html,dcc
from nav_bar_simple import render_navbar


card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}
style ={"position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)","color": "white"}
style1 ={"position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)","color": "blue"}

card1 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Admin Panel", className="card-title"),
                    html.Hr(),
                    html.P("This card has some text content", className="card-text",),
                ]
            )
        ),
        dbc.Card(
            html.A(html.Div(className="fas fa-cogs fa-3x", style=style),href = "#"),
            #className="bg-primary",
            style={"maxWidth": 75,"background-color": "#9E9E9E"},
        ),
    ],
    className="mt-4 mr-3 shadow",
)

card2 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Documents", className="card-title"),
                    html.Hr(),
                    html.P("This card has some text content", className="card-text",),
                ]
            )
        ),
        dbc.Card(
                html.A(html.Div(className="fa fa-folder-open fa-3x",style = style1),href = "#"),
            style={"maxWidth": 75,"background-color": "#FFFF00"},
        ),
    ],
    className="mt-4 mr-3 shadow",
)

card3 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Use cases", className="card-title"),
                    html.Hr(),
                    html.P("This card has some text content", className="card-text",),
                ]
            )
        ),
        dbc.Card(
            html.Div([html.A(
                html.Div(className="fas fa-check-circle fa-3x", style=style),
                id="fade-button",
                n_clicks=0,
                href="#",
                
            ),
            dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Use Cases")),
                dbc.ModalBody(dcc.RadioItems(options=[{'label': 'New York City', 'value': 'NYC'},
                                                        {'label': 'Montreal', 'value': 'Montreal'},
                                                        {'label': 'San Francisco', 'value': 'SF'}],
                                              value='Montreal')),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal",
            is_open=False,
        )]),
            style={"maxWidth": 75,"background-color": "#008000"},
        )
    ],
    className="mt-4 shadow",
)

# Define the layout
cards = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(children = [dbc.Col(card1),dbc.Col(card2),dbc.Col(card3)])
                ],
                className="d-flex justify-content-center align-items-center"
            ),
            style={"height": "400px","margin-left": "2rem", "margin-right": "2rem","background-color": "#EDEDED"}
        )
    ]
)

navbar = render_navbar()
app.layout = html.Div(children = [navbar,html.Br(),html.Br(),cards])