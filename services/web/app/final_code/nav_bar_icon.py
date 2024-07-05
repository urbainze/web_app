import dash_bootstrap_components as dbc
from dash import html



# Define navbar styles
navbar_style = {
    'background-image': 'linear-gradient(89.84deg, #492d7b 0.11%, #8c2c84 14.07%, #ce2935 72.91%, #ec7f31 99.84%)',
    'padding': '10px','height': '50px'  # Adjust padding as needed
}

def render_navbar(brand_name:str = "CSGroup", brand_color:str = "#117be9"):
    navbar = dbc.NavbarSimple(children = [
        dbc.NavItem(children = [html.I(className="fas fa-question mt-4 mb-4",style = {"color":"#6c757d"},id="open-offcanvas", n_clicks=0),
                   dbc.Tooltip("Help", target="open-offcanvas")]),
        dbc.Offcanvas(
            html.P(
                "This is the content of the Offcanvas. "
                "Close it by clicking on the close button, or "
                "the backdrop."
            ),
            id="offcanvas",
            title="Title",
            is_open=False,
            placement="end",  # Set placement to "end" for right side
        )
    ],
        brand="CS Group",
        style = navbar_style,
        brand_href="#",
        #color=brand_color,
        sticky='top',
        #links_left=True,
        dark=True,
        #expand=True
    )
    return navbar