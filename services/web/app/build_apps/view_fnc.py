import dash_bootstrap_components as dbc
from build_apps.chatbot_controler import register_callbacks
from dash import Dash , html
from build_apps.nav_bar_simple import render_navbar
from build_apps.intermediate_page import intermediate_page

#we define the 3 cards components
card1,card2,card3 = intermediate_page()

#here we put the 3 cards components in a new card for the admin user view
cards1 = html.Div(
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

#here we put the 3 cards components in a new card for the simple user view
cards2 = html.Div(
    [
        dbc.Card(
                dbc.CardBody(
                [
                    dbc.Row(children = [dbc.Col(card3)])
                ],
                className="d-flex justify-content-center align-items-center"
            ),
            style={"height": "400px","margin-left": "2rem", "margin-right": "2rem","background-color": "#EDEDED"}
        )
    ]
)

navbar = render_navbar()

def dash_apps(is_admin=False):
    if is_admin == True:
        return html.Div(children = [navbar,html.Br(),html.Br(),cards1])
    else:
        return html.Div(children = [navbar,html.Br(),html.Br(),cards2])