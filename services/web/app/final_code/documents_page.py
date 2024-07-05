import dash_bootstrap_components as dbc
from dash import  html
from nav_bar_search import render_navbar

# Define tooltips for each icon
tooltips = {
    "/files": "files",
    "/logout": "Logout",
    "/return": "Return",
    "/users": "Users",
    "/history":"History"
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
                    "files",
                    target="files-tooltip",
                    placement="right"
                ),
                html.A(
                    id="files-tooltip",
                    href="/files",
                    children=html.I(className="fas fa-file mt-1 mb-4",style = {"color":"#6c757d"})
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
                    "Return",
                    target="return-tooltip",
                    placement="right"
                ),
                html.A(
                    id="return-tooltip",
                    href="/return",
                    children=html.I(className="fas fa-backward mt-4 mb-4",style = {"color":"#6c757d"})
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