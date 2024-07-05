import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
from dash import html,dcc


log_out = html.A(
                    id="logout-tooltip",
                    href="/logout",
                    children=html.I(className="fas fa-sign-out-alt mt-4 mb-4",style = {"color":"#FFFFFF"})
                )
# Define navbar styles
navbar_style = {
    'background-image': 'linear-gradient(89.84deg, #492d7b 0.11%, #8c2c84 14.07%, #ce2935 72.91%, #ec7f31 99.84%)',
    'padding': '10px','height': '50px'  # Adjust padding as needed
}


'''def render_navbar(brand_name:str = "CSGroup", brand_color:str = "#117be9"):
    navbar = dbc.NavbarSimple(
        children = [html.Div(id = 'username-display',style={'color': 'white', 'fontWeight': 'bold','text-align': 'center'}),log_out],
        brand=brand_name,
        brand_href="#",
        style = navbar_style,
        #color=brand_color,
        sticky='top',
        #links_left=True,
        dark=True,
        #expand=True
    )
    return navbar'''

def render_navbar(brand_name: str = "CSGroup", brand_color: str = "#117be9"):
    navbar = dbc.NavbarSimple(
        children=[
            # Flexbox approach with space between email and logout
            html.Div(  # Wrapper for flexbox control
                children=[
                    dbc.NavbarBrand(  # Use for email display (empty initially)
                        id='username-display',
                        className='mr-auto'  # Right-align email
                    ),
                    log_out  # Logout button (assuming it's a defined component)
                ],
                className='d-flex justify-content-center align-items-center'  # Center both horizontally and vertically
            )
        ],
        brand=brand_name,
        brand_href="#",
        style=navbar_style,  # Assuming `navbar_style` is defined elsewhere
        sticky='top',
        dark=True
    )

    return navbar