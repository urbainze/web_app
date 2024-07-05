import dash_bootstrap_components as dbc
from dash import  html
from nav_bar_icon import render_navbar


# Define tooltips for each icon
tooltips = {
    "/settings": "Settings",
    "/logout": "Logout",
    "/dashboard": "Dashboard",
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
                    "Dashboard",
                    target="dashboard-tooltip",
                    placement="right"
                ),
                html.A(
                    id="dashboard-tooltip",
                    href="/dashboard",
                    children=html.I(className="fas fa-chart-line mt-4 mb-4",style = {"color":"#6c757d"})
                ),
                
                dbc.Tooltip(
                    "Users",
                    target="users-tooltip",
                    placement="right"
                ),
                html.A(
                    id="users-tooltip",
                    href="/users",
                    children=html.I(className="fas fa-users mt-4 mb-4",style = {"color":"#6c757d"}),
                ),
                dbc.Tooltip(
                    "History",
                    target="history-tooltip",
                    placement="right"
                ),
                html.A(
                    id="history-tooltip",
                    href="/history",
                    children=html.I(className="fas fa-history mt-4 mb-4",style = {"color":"#6c757d"}),
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