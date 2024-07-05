import dash_bootstrap_components as dbc
from dash import html



def search_bar():
    search = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search ...")),
            dbc.Col(
                dbc.Button(
                    html.I(className="fas fa-search mt-4 mb-4"), color='#A8A8A8', className="ms-2", n_clicks=0
                ),
                width="auto",
            ),
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )
    return search