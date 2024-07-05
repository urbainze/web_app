import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from nav_bar_icon import render_navbar



# Define tooltips for each icon
tooltips = {
    "/settings": "Settings",
    "/logout": "Logout",
    "/chat": "Chat"
}

# Define the layout with inline CSS and tooltips
side_bar = html.Div(
    children=[
        html.Div(
            className="sidebar",
            style={
                'width': '5%',
                'height': '100vh',
                'float': 'left',
                'padding': '20px',
                'background-color': ' #A8A8A8 '
            },
            children=[
                dbc.Tooltip(
                    "Settings",
                    target="settings-tooltip",
                    placement="right"
                ),
                html.A(
                    id="settings-tooltip",
                    href="/settings",
                    children=html.I(className="fas fa-cog mt-1 mb-4",style = {"color":"#6c757d"})
                ),
                
                dbc.Tooltip(
                    "Logout",
                    target="logout-tooltip",
                    placement="right"
                ),
                html.A(
                    id="logout-tooltip",
                    href="/logout",
                    children=html.I(className="fas fa-sign-out-alt mt-4 mb-4",style = {"color":"#6c757d"})
                ),
                
                dbc.Tooltip(
                    "Chat",
                    target="chat-tooltip",
                    placement="right"
                ),
                html.A(
                    id="chat-tooltip",
                    href="/chat",
                    children=html.I(className="fas fa-comment fa-3x mt-4 mb-4",style = {"color":"#6c757d"})
                )
            ]
        )
    ],
    style={
        "tooltip-inner": {"color": "blue"}  # Inline CSS for tooltip text color
    }
)

navbar = render_navbar()
app.layout  =  html.Div(children = [navbar,side_bar ])