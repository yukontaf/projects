import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import datetime
import plotly.graph_objects as go
import plotly.express as px
import sys

sys.path.insert(0, "/Users/glebsokolov/projects/stockPlot/assets")
from data import *
from styles import *

import yfinance as yf
import pandas as pd
from dash import *

stylesheet1 = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(external_stylesheets=[stylesheet1, dbc.themes.BOOTSTRAP])
ticker_name = html.Div(
    [
        dbc.Label("Ticker Name", html_for="ticker-name"),
        dbc.Input(type="text", id="ticker-name"),
    ]
)


sidebar = html.Div(
    [html.H2("Parameters", style=TEXT_STYLE), html.Hr(), ticker_name],
    style=SIDEBAR_STYLE,
)
fig1 = dcc.Graph(id="fig1")

c_first_row = dbc.Row(
    [
        dbc.Col(dbc.Card(fig1), width=6),
    ]
)

content = html.Div(
    [
        html.H2("Analytics Dashboard Template", style=TEXT_STYLE),
        c_first_row,
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)
app.layout = html.Div(
    [
        sidebar,
        content,
        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)


@app.callback(
    Output(component_id="fig1", component_property="figure"),
    Input("interval-component", "n_intervals"),
)
def refresh_fig1(i):
    df = msft_history.iloc[: i + 1, :]
    fig1 = go.Figure(
        data=[
            go.Candlestick(
                x=df["Datetime"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )
    return fig1


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
