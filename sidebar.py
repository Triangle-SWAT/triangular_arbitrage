
import dash_bootstrap_components as dbc
from dash import dcc, html

SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 62.5,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "height": "100%",
        "z-index": 1,
        "overflow-x": "hidden",
        "transition": "all 0.5s",
        "padding": "0.5rem 1rem",
        "background-color": "#f8f9fa",
    }

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Home Screen",
                    href="/home-screen",
                    id="home-screen-link"
                ),
                dbc.NavLink("Blotter", href="/blotter", id="blotter-link"),
                dbc.NavLink("Errors", href="/errors", id="errors-link"),
            ],
            vertical=True,
            pills=True
        ),
        html.P(children="False", id='ibkr-async-conn-status'),
        html.Div(children='', id='placeholder-div'),
        html.Button('Trade', id='trade-button', n_clicks=0),
        html.P(children='', id='uses-async')
    ],
    id="sidebar",
    style=SIDEBAR_STYLE
)
