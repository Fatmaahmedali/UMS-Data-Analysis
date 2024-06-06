import dash
from dash import html, dcc, Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_extensions as de

url = "https://assets2.lottiefiles.com/private_files/lf30_uxql6h6k.json"
options = dict(loop=True, autoplay=True, renderSettings=dict(preserveAspectRatio='xMidYMid slice'))

app3 = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB,
                                                                dbc.icons.FONT_AWESOME,
                                                                dbc.icons.BOOTSTRAP])
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.I(className="fa-solid fa-chart-simple"),
                html.Div(page["name"], className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="bg-light",
    style={
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        'height': '765px',
        'position': 'fixed',
        'width': '145px'
    }
)

app3.layout = dbc.Container([
    dcc.Store(id='store_uid'),
    dbc.Row([
        dbc.Col([
            sidebar
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2, style={'padding': '0px', 'margin': '0px'}),
        dbc.Col([
            dash.page_container
        ], xs=8, sm=8, md=11, lg=10, xl=10, xxl=10)
    ])

], fluid=True)

if __name__ == "__main__":
    app3.run(debug=True)
