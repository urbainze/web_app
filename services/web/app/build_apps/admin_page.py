import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import dash
import pandas as pd
from dash import dcc
from build_apps import monitoring_page # this page just render a blank card  
#from build_apps import dash_table # we import the function to handle user right in a table 

#------------------------------------------------------------------------------------------
#this page is the one to manage users right 
#and monitor some aspects of the app like the adware usage , logs , finance , latency ....
#in this page you can also configure the server 
#------------------------------------------------------------------------------------------
'''# Function to load data from the SQLite database
def load_data():
    users = User.query.all()
    df = pd.DataFrame([(u.uid, u.email, u.password, u.is_admin) for u in users], columns=['uid', 'email', 'password', 'is_admin'])
    return df

# Load data from SQLite database
df = load_data()

#the layout for the user database display
# Layout of the Dash app
table_layout = html.Div([
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
        page_size = 5,
        style_table={'overflowX': 'auto'}
    ),
    #dbc.Button("Modify", id="modify-button", n_clicks=0, style={'margin': '20px'}),
    #dbc.Button("Drop", id="drop-button", n_clicks=0, style={'margin': '20px'}),
    #dbc.Button("Add New User", id="add-button", n_clicks=0),
    dbc.Row(
        [
            dbc.Col(dbc.Button(children=html.I(className="fas fa-edit", style={'color': 'black', 'fontSize': '24px'}),
                               id="modify-button", n_clicks=0,
                               style={'background-color': 'transparent', 'border': 'none'}),className="d-flex justify-content-center"),
            dbc.Col(dbc.Button(html.I(className="fas fa-trash-alt",style={'color': 'red', 'font-size': '16px'}),
                               id="drop-button", n_clicks=0,
                               style={'background-color': 'transparent', 'border': 'none'}),className="d-flex justify-content-center"),
            dbc.Col(dbc.Button(html.I(className="fas fa-plus-circle",
                                      style={'color': 'green', 'font-size': '24px'}),
                               id="add-button", n_clicks=0,
                               style={'background-color': 'transparent', 'border': 'none'}),className="d-flex justify-content-center")
        ],
        justify="center",
        className = "d-flex justify-content-center align-items-center"
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Modify Row"),
            dbc.ModalBody([
                dbc.Label("Email"),
                dbc.Input(id="email-input", type="email"),
                dbc.Label("Password"),
                dbc.Input(id="password-input", type="password"),
                dbc.Label("Is Admin"),
                dbc.Checkbox(id="is-admin-input"),
            ]),
            dbc.ModalFooter(
                [
                    dbc.Button("Save", id="save-button", n_clicks=0),
                    dbc.Button("Cancel", id="cancel-button", n_clicks=0, className="ml-auto")
                ]
            ),
        ],
        id="modal",
        is_open=False,
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Add New User"),
            dbc.ModalBody([
                dbc.Label("Email"),
                dbc.Input(id="new-email-input", type="email"),
                dbc.Label("Password"),
                dbc.Input(id="new-password-input", type="password"),
                dbc.Label("Is Admin"),
                dbc.Checkbox(id="new-is-admin-input"),
            ]),
            dbc.ModalFooter(
                [
                    dbc.Button("Add", id="add-save-button", n_clicks=0),
                    dbc.Button("Cancel", id="add-cancel-button", n_clicks=0, className="ml-auto")
                ]
            ),
        ],
        id="add-modal",
        is_open=False,
    )
])

table_layout = html.Div([
    html.Br(),
    dbc.Row(
        dbc.Col(
            width = 12,
            children = [
                dbc.Card([
                    dbc.CardBody([
                        table_layout
                    ])
                ])
            ],
            style={'height': '84vh'}
        )
    )
])'''



#--------------------------------------------------------------------
#here we define the nav bar style 
#--------------------------------------------------------------------
navbar_style = {
    'background-image': 'linear-gradient(89.84deg, #492d7b 0.11%, #8c2c84 14.07%, #ce2935 72.91%, #ec7f31 99.84%)',
    'padding': '10px','height': '50px'  # Adjust padding as needed
}

def render_navbar(brand_name:str = "CSGroup", brand_color:str = "#117be9"):
    navbar = dbc.NavbarSimple(children = [
        html.Div(
        dbc.DropdownMenu(
                       children=[
                           dbc.DropdownMenuItem("Hardware", href="#"),
                           dbc.DropdownMenuItem("Carbone", href="#"),
                           dbc.DropdownMenuItem("Logs", href="#"),
                           dbc.DropdownMenuItem("Finance", href="#"),
                           dbc.DropdownMenuItem("Latency", href="#"),
                           dbc.DropdownMenuItem("Quality", href="#"),
                       ],
                       nav=True,
                       in_navbar=True,
                       label="Monitoring",
                   ), 
                   className=" mt-4 mb-4 mr-5"
                ),
        html.Div(
        dbc.DropdownMenu(
                       children=[
                           dbc.DropdownMenuItem("Page 2", href="#"),
                           dbc.DropdownMenuItem("Page 3", href="#"),
                       ],
                       nav=True,
                       in_navbar=True,
                       label="Models",
                   ), 
                   className=" mt-4 mb-4 mr-5"
                ),
        
        dbc.NavItem(children = [html.I(className="fas fa-question mt-4 mb-4 ml-3",style = {"color":"#6c757d"},id="open-offcanvas", n_clicks=0),
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
#--------------------------------------------------------------------
#here we define the side  bar style 
#--------------------------------------------------------------------
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
                    "Settings",
                    target="settings-tooltip",
                    placement="right"
                ),
                html.A(
                    id="settings-tooltip",
                    href="#",
                    children=html.I(className="fas fa-cog mt-1 mb-4",style = {"color":"#F7F6FB"})
                ),
                
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
                    "Servers",
                    target="dashboard-tooltip",
                    placement="right"
                ),
                html.A(
                    id="dashboard-tooltip",
                    href="#",
                    children=html.I(className="fas fa-server  mt-4 mb-4",style = {"color":"#F7F6FB"})
                ),
                
                dbc.Tooltip(
                    "Users",
                    target="users-tooltip",
                    placement="right"
                ),
                html.A(
                    id="users-tooltip",
                    href="#",
                    children=html.I(className="fas fa-users mt-4 mb-4",style = {"color":"#F7F6FB"}),
                ),
                dbc.Tooltip(
                    "History",
                    target="history-tooltip",
                    placement="right"
                ),
                html.A(
                    id="history-tooltip",
                    href="#",
                    children=html.I(className="fas fa-history mt-4 mb-4",style = {"color":"#F7F6FB"}),
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

# we instantiate the function for the navbar
navbar = render_navbar()
# this is the layout for this page
def page1_layout():
    return html.Div([
        navbar,
        side_bar,
        dcc.Store(id='admin-content-store', data='default'),
        html.Div(id='admin-content', style={'margin-left': '6%'})
        ])

# we define all the callback which will be used for this page 
# we'll call this function in the create_app.py 
def register_admin_callbacks(app):
    @app.callback(
        Output('admin-content-store', 'data'),
        [Input('settings-tooltip', 'n_clicks'),
         Input('dashboard-tooltip', 'n_clicks'),
         Input('users-tooltip', 'n_clicks'),
         Input('history-tooltip', 'n_clicks')],
        prevent_initial_call=True
    )
    def update_admin_content_store(n_settings, n_dashboard, n_users, n_history):
        ctx = dash.callback_context

        if not ctx.triggered:
            return 'default'

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'settings-tooltip':
            return 'settings'
        elif button_id == 'dashboard-tooltip':
            return 'dashboard'
        elif button_id == 'users-tooltip':
            return 'users'
        elif button_id == 'history-tooltip':
            return 'history'
        return 'default'

    @app.callback(
        Output('admin-content', 'children'),
        Input('admin-content-store', 'data')
    )
    def render_admin_content(section):
        if section == 'settings':
            return monitoring_page.monitoring_layout
        elif section == 'dashboard':
            return monitoring_page.monitoring_layout
        elif section == 'users':
            return monitoring_page.monitoring_layout
        elif section == 'history':
            return monitoring_page.monitoring_layout
        else:
            return monitoring_page.monitoring_layout
               

