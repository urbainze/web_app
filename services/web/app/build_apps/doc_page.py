import dash_bootstrap_components as dbc
from dash import Input, Output, State, html , dcc
from build_apps import monitoring_page
import base64
import dash

#------------------------------------------------------------------------------------------
#this page is the one to documents submited for the database  
#you can also see the documents uploaded 
#
#------------------------------------------------------------------------------------------
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
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search ...")),
        dbc.Col(
            dbc.Button(
                html.I(className="fas fa-search mt-4 mb-4"), color='#A8A8A8', className="ms-1", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


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
                'background-color': ' #4723D9 '
            },
            children=[
                dbc.Tooltip(
                    "files",
                    target="files-tooltip",
                    placement="right"
                ),
                html.A(
                    id="files-tooltip",
                    href="#",
                    children=html.I(className="fas fa-file mt-1 mb-4",style = {"color":"#F7F6FB"})
                ),
                dbc.Tooltip(
                    "upload documents",
                    target="upload-file",
                    placement="right"
                ),
                dcc.Upload(dbc.Button(
                id="upload-file",
                children=html.I(className="fas fa-upload mt-4 mb-4",style = {"color":"#F7F6FB"}),
                color="Light",
                style={"padding": "0px"},
            )),
                
                dbc.Tooltip(
                    "Logout",
                    target="logout-tooltip",
                    placement="right"
                ),
                html.A(
                    id="logout-tooltip",
                    href="/logout",
                    children=html.I(className="fas fa-sign-out-alt mt-4 mb-4",style = {"color":"#F7F6FB"})
                ),
                
                dbc.Tooltip(
                    "Return",
                    target="return-tooltip",
                    placement="right"
                ),
                html.A(
                    id="return-tooltip",
                    href="/dashboard1/",
                    children=html.I(className="fas fa-backward mt-4 mb-4",style = {"color":"#F7F6FB"})
                )
            ]
        )
    ],
    style={
        "tooltip-inner": {"color": "blue"}  # Inline CSS for tooltip text color
    }
)
# we instantiate the navbar function 
navbar = render_navbar()

# we define the layout for this page 
def doc_layout():
    return html.Div([
        navbar,
        side_bar,
        dcc.Store(id='doc-content-store', data='default'),
        html.Div(id='doc-content', style={'margin-left': '6%'})
        ])
# we define the callbacks for this page 
def register_doc_callbacks(app):
    @app.callback(
        Output('doc-content-store', 'data'),
        [Input('files-tooltip', 'n_clicks'),],
        prevent_initial_call=True
    )
    def update_admin_content_store(n_settings, n_dashboard, n_users, n_history):
        ctx = dash.callback_context

        if not ctx.triggered:
            return 'default'

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'files-tooltip':
            return 'files'
        return 'default'

    @app.callback(
        Output('doc-content', 'children'),
        Input('doc-content-store', 'data')
    )
    def render_admin_content(section):
        if section == 'files':
            return monitoring_page.monitoring_layout
        else:
            return monitoring_page.monitoring_layout




