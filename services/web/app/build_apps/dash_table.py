from dash import html,dash_table 
import dash_bootstrap_components as dbc
import pandas as pd
from dash import  html,Input,Output,State,dash_table
from werkzeug.security import generate_password_hash
import dash
import sqlite3




# Database file path
'''db_file = 'C:/Users/uze/Documents/tests/app/instance/mydb.db'

# Function to load data from the SQLite database
def load_data():
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM users", conn)  # Assuming your table is named 'users'
    conn.close()
    return df
# Load data from SQLite database
df = load_data()

#we define the buttons
bt1 = dbc.Button(children=html.I(className="fas fa-edit", style={'color': 'black', 'fontSize': '24px'}),
                               id="modify-button", n_clicks=0,
                               style={'background-color': 'transparent', 'border': 'none'})
bt2  = dbc.Button(html.I(className="fas fa-trash-alt",style={'color': 'red', 'font-size': '16px'}),
                               id="drop-button", n_clicks=0,
                               style={'background-color': 'transparent', 'border': 'none'})
bt3 = dbc.Button(html.I(className="fas fa-plus-circle",
                                      style={'color': 'green', 'font-size': '24px'}),
                               id="add-button", n_clicks=0,
                               style={'background-color': 'transparent', 'border': 'none'})
# Layout of the Dash app
'''table_layout = html.Div([
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        row_selectable='single',
        style_as_list_view=True,
        style_cell={'textOverflow': 'ellipsis','overflow': 'hidden','minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
        style_header={
        'backgroundColor': '#89CFF0',
        'fontWeight': 'bold'
        },
        style_cell_conditional=[
        {'if': {'column_id': 'email'},
         'width': '30%'},
        {'if': {'column_id': 'password'},
         'width': '30%'},],
        selected_rows=[],
        page_size = 5,
        #style_table={'overflowX': 'auto'}
    ),'''
    # Define your table layout
table_layout = html.Div([
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        row_selectable='single',
        style_as_list_view=True,
        style_cell={'textOverflow': 'ellipsis', 'overflow': 'hidden', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
        style_header={
            'backgroundColor': '#89CFF0',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'uid'}, 'width': '5%','paddingLeft': '5px'},  # Adjust width of 'uid' column
            {'if': {'column_id': 'email'}, 'width': '40%', 'paddingRight': '50px'},  # Add spacing to 'email' column
            {'if': {'column_id': 'password'}, 'width': '40%'}
        ],
        selected_rows=[],
        page_size=10,
    ),
    #dbc.Button("Modify", id="modify-button", n_clicks=0, style={'margin': '20px'}),
    #dbc.Button("Drop", id="drop-button", n_clicks=0, style={'margin': '20px'}),
    #dbc.Button("Add New User", id="add-button", n_clicks=0),
   
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

tablelayout = html.Div([
    html.Div([bt1,bt2,bt3]),
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
])


# Function to load data from the SQLite database


# Layout of the Dash app


#the callbacks for the dash table 
def register_users_callbacks(app):
    # Callbacks to handle the functionality
    @app.callback(
        Output('modal', 'is_open'),
        [Input('modify-button', 'n_clicks'), Input('cancel-button', 'n_clicks'), Input('save-button', 'n_clicks')],
        [State('modal', 'is_open'), State('data-table', 'selected_rows')]
    )
    def toggle_modal(modify_n_clicks, cancel_n_clicks, save_n_clicks, is_open, selected_rows):
        ctx = dash.callback_context

        if not ctx.triggered:
            return is_open

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'modify-button' and selected_rows:
            return True
        elif button_id == 'save-button' or button_id == 'cancel-button':
            return False
        return is_open

    @app.callback(
        Output('add-modal', 'is_open'),
        [Input('add-button', 'n_clicks'), Input('add-cancel-button', 'n_clicks'), Input('add-save-button', 'n_clicks')],
        [State('add-modal', 'is_open')]
    )
    def toggle_add_modal(add_n_clicks, add_cancel_n_clicks, add_save_n_clicks, is_open):
        ctx = dash.callback_context

        if not ctx.triggered:
            return is_open

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add-button':
            return True
        elif button_id == 'add-save-button' or button_id == 'add-cancel-button':
            return False
        return is_open

    @app.callback(
        [Output('email-input', 'value'), Output('password-input', 'value'), Output('is-admin-input', 'value')],
        [Input('modify-button', 'n_clicks')],
        [State('data-table', 'selected_rows'), State('data-table', 'data')]
    )
    def populate_modal(modify_n_clicks, selected_rows, table_data):
        if modify_n_clicks and selected_rows:
            row = selected_rows[0]
            row_data = table_data[row]
            return row_data['email'], row_data['password'], row_data['is_admin']
        return '', '', False

    @app.callback(
        Output('data-table', 'data'),
        [Input('save-button', 'n_clicks'), Input('drop-button', 'n_clicks'), Input('add-save-button', 'n_clicks')],
        [State('email-input', 'value'), State('password-input', 'value'), State('is-admin-input', 'value'), State('new-email-input', 'value'), State('new-password-input', 'value'), State('new-is-admin-input', 'value'), State('data-table', 'selected_rows'), State('data-table', 'data')]
    )
    def update_table(save_n_clicks, drop_n_clicks, add_save_n_clicks, email, password, is_admin, new_email, new_password, new_is_admin, selected_rows, table_data):
        ctx = dash.callback_context

        if not ctx.triggered:
            return table_data

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        if button_id == 'save-button' and selected_rows:
            row = selected_rows[0]
            row_id = table_data[row]['uid']  # Assuming 'uid' is the primary key column
            cursor.execute("""
                UPDATE users
                SET email = ?, password = ?, is_admin = ?
                WHERE uid = ?
            """, (email, password, is_admin, row_id))
            conn.commit()

        elif button_id == 'drop-button' and selected_rows:
            row = selected_rows[0]
            row_id = table_data[row]['uid']
            cursor.execute("DELETE FROM users WHERE uid = ?", (row_id,))
            conn.commit()

        elif button_id == 'add-save-button':
            cursor.execute("""
                INSERT INTO users (email, password,is_admin)
                VALUES (?, ?,?)
            """, (new_email, generate_password_hash(new_password),is_admin))
            conn.commit()
        

        # Reload data from the database
        df = load_data()
        return df.to_dict('records')'''