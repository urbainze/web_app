import dash_bootstrap_components as dbc
from search_bar import search_bar




# Define navbar styles
navbar_style = {
    'background-image': 'linear-gradient(89.84deg, #492d7b 0.11%, #8c2c84 14.07%, #ce2935 72.91%, #ec7f31 99.84%)',
    'padding': '10px','height': '50px' # Adjust padding as needed
}

def render_navbar(brand_name:str = "CSGroup", brand_color:str = "#117be9"):
    navbar = dbc.NavbarSimple(children = [
        search_bar
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