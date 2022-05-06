import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import datetime
import plotly.graph_objects as go
import plotly.express as px
import sys
import yfinance as yf


sys.path.insert(0, "/Users/glebsokolov/projects/stockPlot/assets")
from data import *
from styles import *

import yfinance as yf
import pandas as pd

stylesheet1 = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(external_stylesheets=[stylesheet1, dbc.themes.BOOTSTRAP])
slider = dcc.Slider(3, 15, 1, value=5, id="ma")
ticker_name = html.Div(
    dbc.FormFloating(
        [
            dbc.Input(type="text", id="ticker-name", debounce=True),
            dbc.Label("Ticker Name"),
        ]
    )
)


def breaks(num):
    return [html.Br()] * num


sidebar = html.Div(
    [
        html.H2("Parameters", style=TEXT_STYLE),
        html.Hr(),
        dbc.Card(ticker_name),
        *breaks(1),
        dbc.Card(dbc.CardBody([html.P("Choose MA period"), slider])),
    ],
    style=SIDEBAR_STYLE,
)
fig1 = dcc.Graph(id="fig1")

c_first_row = dbc.Row(
    [
        dbc.Col(dbc.Card(fig1)),
    ]
)

content = html.Div(
    [
        html.H2("Live Stock Exchange Chart", style=TEXT_STYLE),
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
    [
        Input("ticker-name", "value"),
        Input("interval-component", "n_intervals"),
        Input("ma", "value"),
    ],
)
def refresh_fig1(name, i, smoothing):
    data = yf.Ticker(name)
    df = prettify(data).iloc[i : 60 + i, :]
    moving_average = (
        df.iloc[1:, :]
        .rolling(window=smoothing)
        .mean()
        .apply(lambda x: (x["Open"] + x["High"] + x["Low"] + x["Close"]) / 4, axis=1)
    )
    fig1 = go.Figure(
        data=[
            go.Candlestick(
                x=df["Datetime"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="OHLC",
            )
        ]
    )
    fig1.update_layout(height=650, title=f"{name.upper()}")
    fig1.add_trace(
        go.Scatter(
            x=df["Datetime"], y=moving_average, name=f"MA{smoothing}", mode="lines"
        )
    )
    return fig1


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
