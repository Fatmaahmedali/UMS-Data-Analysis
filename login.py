from flask import Flask, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_mysqldb import MySQL
import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import dash_extensions as de
import secrets
from flask import session
import redis
# from StudentInterface.pages.pg1 import store_uid_student
import urllib.parse

from StudentInterface.home import app1 as app1
from DoctorInterface.home import app2 as app2
from DecisionMaker.home import app3 as app3

# from app import app1

secret_key = secrets.token_hex(16)
from dash.dependencies import Input, Output, State

# Set up Flask app
server = Flask(__name__)
server.config['SECRET_KEY'] = secret_key

# Set up MySQL database
server.config['MYSQL_HOST'] = "127.0.0.1"
server.config['MYSQL_USER'] = "root"
server.config['MYSQL_DB'] = "mydb"
mysql = MySQL(server)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)


# Define User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


# Define user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# For Lottie Graphics
url = "https://assets2.lottiefiles.com/packages/lf20_G471niMHMD.json"
options = dict(loop=True, autoplay=True, renderSettings=dict(preserveAspectRatio='xMidYMid slice'))

# Set up Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME,
                                                               dbc.icons.BOOTSTRAP])

# Configure server-side sessions
app.server.config['SESSION_TYPE'] = 'filesystem'
app.server.config['SESSION_FILE_DIR'] = '/tmp'
# session(app.server)# server = app1.server

# # Mount apps at their route prefixes
# app.server.mount('/app1', server)
# app.server.mount('/app2', app2.server)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(id='hidden_div_for_redirect_callback'),
    dcc.Store(id='store_uid_student')
])

login_layout = html.Div([
    html.Div(de.Lottie(options=options, width="25%", height="25%", url=url)),
    html.Div(dcc.Input(id="email-input", type="text", placeholder="Email", className="inputbox1",
                       style={'margin-left': '35%', 'width': '450px', 'height': '45px',
                              'padding': '10px', 'margin-top': '60px',
                              'font-size': '16px', 'border-width': '3px', 'outline': 'none',
                              'border': '3px solid rgb(190 179 179 / 25%)', 'border-radius': '5px',
                              'box-shadow': 'rgb(31 84 173) -5px -3px 13px -7px'
                              })),
    html.Div(dcc.Input(id="password-input", type="password", placeholder="Password", className="inputbox2",
                       style={'margin-left': '35%', 'width': '450px', 'height': '45px', 'padding': '10px',
                              'margin-top': '10px', 'font-size': '16px', 'border': '3px solid rgb(190 179 179 / 25%)',
                              'border-radius': '5px', 'outline': 'none',
                              'box-shadow': 'rgb(31 84 173) -5px -3px 13px -7px'
                              })),
    html.Div([
        html.Div(children=[html.Button(['Login'], n_clicks=0, className="me-1 ms-2 text-black-50",
                                       style={
                                           'background': 'none',
                                           'border-width': '3px',
                                           'font-size': '14px',
                                           'border': '2px solid  #5c66d9',
                                           'padding': '10px',
                                           'border-radius': '14px',
                                           'width': '116px'
                                       }, id='login-button'),
                           ],
                 # style={'margin-left': '45%', 'padding-top': '30px'}
                 ),
        dcc.Checklist(
            id='check',
            options=[{'label': 'As A Decision Maker', 'value': 'As A Decision Maker'}],
            value=[],
            style={
                'margin-left': '44px'
            }
        ),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'padding-top': '39px'}),
    html.Div(id='login-error', style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'margin-top': '-84px',
        'margin-right': '245px',
        'color': 'red'
    }),
])


# Define the page content callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login_layout
    elif pathname == '/StudentInterface/home':
        from StudentInterface.pages.pg1 import layout1
        return layout1
    elif pathname == '/StudentInterface/home/pages/pg1':
        from StudentInterface.pages.pg1 import layout1
        return layout1
    elif pathname == '/StudentInterface/home/pages/pg2':
        from StudentInterface.pages.pg2 import layout2
        return layout2
    elif pathname == '/DoctorInterface/home':
        from DoctorInterface.pages.pg1 import layout3
        return layout3
    elif pathname == '/DoctorInterface/home/pages/pg1':
        from DoctorInterface.pages.pg1 import layout3
        return layout3
    elif pathname == '/DoctorInterface/home/pages/pg2':
        from DoctorInterface.pages.pg2 import layout5
        return layout5
    elif pathname == '/DecisionMaker/home':
        from DecisionMaker.pages.pg1 import layout4
        return layout4
    elif pathname == '/DecisionMaker/home/pages/pg1':
        from DoctorInterface.pages.pg1 import layout4
        return layout4


@app.callback(
    [Output('login-error', 'children'),
     Output('hidden_div_for_redirect_callback', 'children'),
     Output('store_uid_student', 'state')],
    [Input('login-button', 'n_clicks')],
    [State('email-input', 'value'),
     State('password-input', 'value'),
     State('check', 'value')]
)
def login(n_clicks, email, password, check):
    if n_clicks == 0:
        return "", "", ""

    # Check if email and password are valid
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT idDoctor, Email, Password, IsDecisionMaker, Role
        FROM doctor
        WHERE Email=%s AND Password=%s
        UNION ALL
        SELECT StudentID, Email, Password, 0 as IsDecisionMaker, Role
        FROM student
        WHERE Email=%s AND Password=%s
    """, (email, password, email, password))
    user = cur.fetchone()

    if user is None:
        return "Invalid email or password", "", ""
    else:
        user_id, email, password, is_decision_maker, role = user
        user_id = str(user[0])
        print("wewe", user_id)
        if is_decision_maker:
            if check:
                # Encode the user ID in the URL
                url1 = '/DecisionMaker/home?user_id={}'.format(urllib.parse.quote(user_id))
                return "", dcc.Location(pathname="/DecisionMaker/home", id='url', refresh=True, href=url1), user_id
            elif role == "doctor":
                if is_decision_maker:
                    url2 = '/DoctorInterface/home?user_id={}'.format(urllib.parse.quote(user_id))
                    return "", dcc.Location(pathname="/DoctorInterface/home", id='url', refresh=True, href=url2), user_id
                else:
                    return "You are not a decision maker", "", ""
            else:
                url3 = '/StudentInterface/home?user_id={}'.format(urllib.parse.quote(user_id))
                print(url3)
                return "", dcc.Location(pathname="/StudentInterface/home", id='url', refresh=True, href=url3), user_id
        elif not is_decision_maker and role == "student":
            if check:
                return "You are not a decision maker", "", ""
            else:
                url4 = '/StudentInterface/home?user_id={}'.format(urllib.parse.quote(user_id))
                return "", dcc.Location(pathname="/StudentInterface/home", id='url', refresh=True, href=url4), user_id
        elif not is_decision_maker and role == "doctor":
            if check:
                if is_decision_maker:
                    url5 = '/DecisionMaker/home?user_id={}'.format(urllib.parse.quote(user_id))
                    return "", dcc.Location(pathname="/DecisionMaker/home", id='url', refresh=True, href=url5), user_id
                else:
                    return "You are not a decision maker", "", ""
            else:
                url6 = '/DoctorInterface/home?user_id={}'.format(urllib.parse.quote(user_id))
                return "", dcc.Location(pathname="/DoctorInterface/home", id='url', refresh=True, href=url6), user_id
        else:
            return "Unknown role", "", ""

    # # Log in user and redirect to main app
    # user_id = str(user[0])
    # user_type = user[1]
    # print(user_id)
    # login_user(User(user_id))
    # # Encode the user ID in the URL
    # url = '/project/home?user_id={}'.format(urllib.parse.quote(user_id))
    # print(url)

    # if n_clicks is not None and user_type == 'student':
    #     return "", dcc.Location(pathname='/project/home', id='login-success1')
    # elif n_clicks is not None and user_type == 'doctor':
    #     return "", dcc.Location(pathname='/DoctorInterface/home', id='login-success2')
    # # elif n_clicks is not None and user_type == 'doctor' and check == 'decision-maker':
    # #     return "", dcc.Location(pathname='/DoctorInterface/decision-maker-home', id='login-success2', href=url)

if __name__ == '__main__':
    app.run_server()
