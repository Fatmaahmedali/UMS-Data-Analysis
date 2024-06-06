import dash
from dash import html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from flask import session

url = "https://assets2.lottiefiles.com/private_files/lf30_uxql6h6k.json"
options = dict(loop=True, autoplay=True, renderSettings=dict(preserveAspectRatio='xMidYMid slice'))

app1 = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME,
                                                                dbc.icons.BOOTSTRAP], )

sidebar = dbc.Nav(
    children=[
        dcc.Markdown(id='output'),
        dbc.NavLink(
            [
                html.I(className="fa-solid fa-chart-simple"),
                html.Div("Registration", className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href='/project/home/pages/pg1?user_id=2v2nN3vhzK',
            active="exact",
        ),
        dbc.NavLink(
            [
                html.I(className="fa-solid fa-chart-simple"),
                html.Div("Performance", className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href='/project/home/pages/pg2?user_id=2v2nN3vhzK',
            active="exact",
        )
    ],
    vertical=True,
    pills=True,
    className="bg-light",
    style={
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        'height': '765px',
        'position': 'fixed',
        'width': '171px'
    }
)

app1.layout1 = dbc.Container([
    dcc.Store(id='store_uid'),
    dbc.Row([
        dbc.Col([
            sidebar
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2, style={'padding': '0px', 'margin': '0px'}),
        dbc.Col([

        ], xs=8, sm=8, md=11, lg=10, xl=10, xxl=10)
    ])
], fluid=True)



if __name__ == "__main__":
    app1.run(server=True, port=8050)
