
import dash_bootstrap_components as dbc
from dash import Dash , html,callback_context,Input, Output, State,dcc
import dash
from flask_login import current_user
from build_apps import admin_page
from dash.exceptions import PreventUpdate
from flask import session
from build_apps.chat_page import chat_callbacks,render_chatbot
from dash import Dash , html
from build_apps.nav_bar_simple import render_navbar
from build_apps.intermediate_page import intermediate_page
from build_apps.admin_page import page1_layout,register_admin_callbacks
from build_apps import doc_page



card1,card2,card3 = intermediate_page()

#we import stuffs for page1


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
            style={"height": "400px","margin-left": "2rem", "margin-right": "2rem","background": "linear-gradient(to right, #e2e2e2, #c9d6ff)"}
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


#@with_current_user
def create_dash_app1(flask_app,name = 'dash1'):
    '''def dash_appss():
        # Define the layout of the Dash app
        return dash_apps()'''

    def register_callbacks(app):
        @app.callback(
            Output("modal", "is_open"),
            [Input("open", "n_clicks"), Input("close", "n_clicks"),Input("submit", "n_clicks")],
            [State("modal", "is_open")],
        )
        def toggle_modal(open_click, close_click, submit_click, is_open):
            if open_click or close_click or submit_click:
                return not is_open
            return is_open
        

        
        # Callback to handle page redirection
        @app.callback(
            Output('url', 'pathname'),
            Input('submit', 'n_clicks'),
            State('radio-items', 'value'),
            prevent_initial_call=True
        )
        def update_url_on_submit(submit_click, selected_value):
            if submit_click:
                if selected_value == 'case1':
                    return '/dashboard1/case1'
                elif selected_value == 'case2':
                    return '/dashboard1/case2'
                elif selected_value == 'case3':
                    return '/dashboard1/case3'
            return dash.no_update
        '''@app.callback(
            Output('url', 'pathname'),
            Input("exit2", "n_clicks")
        )
        def redirect_to_welcome(submit_clicks):
            if submit_clicks:
                return '/dashboard1'
            return dash.no_update'''

        '''@app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')],
            prevent_initial_call=True
        )
        def update_home_layout(pathname):
            is_admin = session.get('is_admin')
            home_layout = home_layout1 if is_admin else home_layout2
            return home_layout'''
        # Set up callbacks for navigation
        @app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
        def display_page(pathname):
            print(f"Pathname: {pathname}")  # Debug statement to check the pathname
            #role = current_user.role
            role = session.get('role')
            if role == 'user' :
                home_layout = home_layout1
            else:
                home_layout = home_layout2
            #home_layout = home_layout1 if is_admin else home_layout2
            if pathname == '/dashboard1/about':
                return admin_layout
            elif pathname == '/dashboard1/doc_page':
                return doc_page.doc_layout()
            elif pathname == '/dashboard1/case1':
                return nyc_layout
            elif pathname == '/dashboard1/case2':
                return montreal_layout
            elif pathname == '/dashboard1/case3':
                return sf_layout
            elif pathname == '/dashboard1':
                return home_layout
            else:
                return home_layout

        @app.callback(
            Output("offcanvas", "is_open"),
            Input("open-offcanvas", "n_clicks"),
            [State("offcanvas", "is_open")],
        )
        def toggle_offcanvas(n1, is_open):
            if n1:
                return not is_open
            return is_open
        @app.callback(Output('username-display', 'children'),Input('username-display', 'id'))
        def update_welcome_message(_):
            email = session.get('email')
            if email:
                 return f'Bienvenue, {email}!'
            else:
                return 'Bienvenue sur le tableau de bord Dash'
 
       
    dash_app = Dash(
        server=flask_app,
        #use_pages=True,
        name=name,
        url_base_pathname="/dashboard1/",
        external_stylesheets=[dbc.themes.BOOTSTRAP,
                              "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css", 
                              dbc.icons.FONT_AWESOME]
    )
    # Define the layouts for each new page
    nyc_layout = render_chatbot()

    montreal_layout = render_chatbot()

    sf_layout = render_chatbot()
    home_layout1 =  html.Div(children = [navbar,html.Br(),html.Br(),cards1])
    home_layout2 =  html.Div(children = [navbar,html.Br(),html.Br(),cards2])
    admin_layout = page1_layout()

    doc_page.register_doc_callbacks(dash_app)
    register_admin_callbacks(dash_app)
    register_callbacks(dash_app)
    chat_callbacks(dash_app)
    # Define the overall app layout
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')])

    return dash_app


