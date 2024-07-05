import base64
from dash import dcc,html
import dash_bootstrap_components as dbc
from dash import html,dcc
from dash import Input, Output, State, html,dcc
import dash


#------------------------------------------------------------------------------------------
#this page is the one that display the chat layout 
# you're redirected to this page after you have chosen your use case 
# 
#------------------------------------------------------------------------------------------
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
                    "Chat",
                    target="chat-tooltip",
                    placement="right"
                ),
                html.A(
                    id="chat-tooltip",
                    href="#",
                    children=html.I(className="fas fa-comment fa-3x mt-4 mb-4",style = {"color":"#F7F6FB"})
                ),
                dbc.Tooltip(
                    "Return",
                    target="open2",
                    placement="right"
                ),
                #html.A(
                    #id="return-tooltip",
                    #href="/dashboard1/",
                    #children=html.I(className="fas fa-backward mt-4 mb-4 ",style = {"color":"#F7F6FB"})
                #),
                html.A(dbc.Button(html.I(className="fas fa-backward mt-4 mb-4 ", style={'color': '#F7F6FB'}), id="open2", n_clicks=0,style={'background-color': 'transparent', 'border': 'none'}),id="dashboard-link"),

                dbc.Modal(
                    [
                        dbc.ModalBody([
                            html.P("Are you satisfied by the service?", className="text-center"),
                            html.Br(),
                            html.Div([
                                html.I(className="fas fa-thumbs-up", style={'color': 'green', 'fontSize': '24px', 'marginRight': '20px'}),
                                html.I(className="fas fa-thumbs-down", style={'color': 'red', 'fontSize': '24px'})
                            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
                            html.Br(),
                            html.Div([
                                html.A(dbc.Button("Exit", id="exit2", className="me-2", n_clicks=0),href = "/dashboard1"),
                                dbc.Button("Cancel", id="close2", className="ms-2", n_clicks=0)
                            ], className="text-center mt-3")
                        ])
                    ],
                    id="modal1",
                    is_open=False,  # Initialize modal as closed
                )
            ]
        )
    ],
    style={
        "tooltip-inner": {"color": "blue"}  # Inline CSS for tooltip text color
    }
)
# we instatiate the navbar function
navbar =  render_navbar()

# this function is for the prompt , the part where user can write to the chat and validate 
def render_chat_input():
    chat_input = html.Div(
        style={'position': 'relative', 'display': 'inline-block', 'width': '100%'},
        children=[
            dbc.Input(id="user-input", placeholder="Send a message...", type="text", style={'paddingLeft': '40px', 'paddingRight': '40px', 'width': '100%'}),
            dbc.Button(id="submit", children=">", color="secondary", style={'position': 'absolute', 'right': '0px', 'top': '0px', 'bottom': '0px', 'borderTopLeftRadius': '0', 'borderBottomLeftRadius': '0'}),
        ]
    )
    return chat_input
# this function define how the messages are rendered and the icons displayed 
def render_textbox(text:str, box:str = "AI"):
    with open('human.jpg', 'rb') as image_file:
        human_ig = base64.b64encode(image_file.read()).decode('utf-8')
    with open('robot.png', 'rb') as image_file:
        robot_ig = base64.b64encode(image_file.read()).decode('utf-8')
    text = text.replace(f"ChatBot:", "").replace("Human:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
        'border': '0px solid'
    }

    if box == "human":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        thumbnail_human = html.Img(
            src=f'data:image/png;base64,{human_ig}',
            style={
                "border-radius": 50,
                "height": 36,
                "margin-left": 5,
                "float": "right",
            },
        )
        textbox_human = dbc.Card(text, style=style, body=True, color="success", inverse=True)
        return html.Div([thumbnail_human, textbox_human])

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=f'data:image/png;base64,{robot_ig}',
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="#cad1cf", inverse=False)

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")
    
#layout for displaying the conversation 
chatbot_layout = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)



# this function is the overall layout for all the content of the chat page 
def render_chatbot():
    return html.Div([
        navbar,
        side_bar,
        dcc.Store(id="store-conversation", data=""),
        html.Div(
            [
                html.Br(),
                dbc.Container(
                    fluid=True,
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    width=12,
                                    children=dbc.Card(
                                        [
                                            #dbc.CardHeader("World map"),
                                            dbc.CardBody(
                                                [
                                                    #html.Div(id='div-vis'),
                                                    chatbot_layout,
                                                    html.Div(render_chat_input(), style={'margin-left': '70px', 'margin-right': '70px', 'margin-bottom': '20px'}),
                                                    dbc.Spinner(html.Div(id="loading-component"))
                                                ]
                                            )
                                        ],
                                        style={'height': '84vh'}
                                    )
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ])
# here we define the callbacks for this page 
def chat_callbacks(app):
    # Run the app
    @app.callback(
        Output(component_id="display-conversation", component_property="children"), 
        Input(component_id="store-conversation", component_property="data")
    )
    def update_display(chat_history):
        return [
            render_textbox(x, box="human") if i % 2 == 0 else render_textbox(x, box="AI")
            for i, x in enumerate(chat_history.split("<split>")[:-1])
        ]


    @app.callback(
    Output(component_id="user-input", component_property="value"),
    Input(component_id="submit", component_property="n_clicks"), 
    Input(component_id="user-input", component_property="n_submit"),
    )
    def clear_input(n_clicks, n_submit):
        return ""

    @app.callback(
        Output(component_id="store-conversation", component_property="data"), 
        Output(component_id="loading-component", component_property="children"),
        Input(component_id="submit", component_property="n_clicks"), 
        Input(component_id="user-input", component_property="n_submit"),
        State(component_id="user-input", component_property="value"), 
        State(component_id="store-conversation", component_property="data"),
    )
    def run_chatbot(n_clicks, n_submit, user_input, chat_history):
        if n_clicks == 0 and n_submit is None:
            return "", None

        if user_input is None or user_input == "":
            return chat_history, None
    
        chat_history += f"Human: {user_input}<split>ChatBot: "
        #result_ai = conversation.predict(input=user_input)
        model_output = "ok"
        chat_history += f"{model_output}<split>"
        return chat_history, None

    @app.callback(
    Output("modal1", "is_open"),
    Output("dashboard-link", "href"),
    Input("open2", "n_clicks"), 
    Input("close2", "n_clicks"), 
    Input("exit2", "n_clicks"),
    State("store-conversation", "data"),
    prevent_initial_call=True
    )
    def toggle_modal(open_clicks, close_clicks, exit_clicks, chat_history):
        ctx = dash.callback_context
        if not ctx.triggered:
            return False, "/dashboard1"
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == "open2":
                if chat_history:
                    messages = chat_history.split("<split>")
                    human_messages = [msg for msg in messages if "Human:" in msg]
                    if len(human_messages) >= 2:
                        return True, "#"
                    else:
                        return False, "/dashboard1"
                else:
                    return False, "/dashboard1"
            elif button_id in ["close2", "exit2"]:
                return False, "/dashboard1"
            return False, "/dashboard1"
    