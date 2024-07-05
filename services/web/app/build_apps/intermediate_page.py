import dash_bootstrap_components as dbc
from dash import html,dcc




# we define here the 3 card displayed after you get loged in the app
def intermediate_page():
    card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
    }
    style ={"position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)","color": "white"}
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
                dcc.Link(html.Div(id = "btn1",className="fas fa-cogs fa-3x", style=style),href = "/dashboard1/about"),
                #className="bg-primary",
                style={"maxWidth": 75,"background": "#4723D9"},
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
                    dcc.Link(html.Div(className="fa fa-folder-open fa-3x",style = style),href = "/dashboard1/doc_page"),
                style={"maxWidth": 75,"background": "#4723D9"},
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
                    id="open",
                    n_clicks=0,
                    #href="#",
                
                ),
                dbc.Modal(
                [
                    #dbc.ModalHeader(dbc.ModalTitle("Use Cases")),
                    dbc.ModalBody([
                        html.H5("Use Cases", className="card-title text-center"),
                        dcc.RadioItems(options=[{'label': 'Use Case1', 'value': 'case1'},
                                                        {'label': 'Use Case2', 'value': 'case2'},
                                                        {'label': 'Use Case3', 'value': 'case3'}],
                                              value='case2',
                                              labelStyle={"display": "block"},
                                              inputStyle={"margin-right": "10px"},
                                              id='radio-items'),
                                              html.Br(),
                                              html.Div([
                                              dbc.Button("Submit", id="submit", className="me-2", n_clicks=0),
                                              dbc.Button("Close", id="close", className="ms-2", n_clicks=0)],
                                              className="text-center mt-3")
                                              ])
                ],
                id="modal",
                is_open=False,
            )]),
                style={"maxWidth": 75,"background": "#4723D9"},
            )
        ],
        className="mt-4 shadow",
    )

    return card1,card2,card3


