import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import datetime
import plotly.graph_objects as go
import plotly.express as px
import sys
from datetime import datetime, timedelta

import yfinance as yf


sys.path.insert(0, "/Users/glebsokolov/projects/stockPlot/assets")
from data import *
from styles import *

import yfinance as yf
import pandas as pd

stylesheet1 = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(external_stylesheets=[stylesheet1, dbc.themes.BOOTSTRAP])

ma_switch = html.Div(
    [
        dbc.Label("Toggle Moving Average"),
        dbc.Checklist(
            options=[
                {"label": "On", "value": True},
            ],
            id="ma-switch",
            switch=True,
        ),
    ]
)

timeframe = dbc.Select(
    id="timeframe",
    options=[
        {"label": "1M", "value": "1/minute"},
        {"label": "5M", "value": "5/minute"},
        {"label": "15M", "value": "15/minute"},
        {"label": "1H", "value": "1/hour"},
    ],
    value="15/minute",
    style={"width": "100px"},
)


slider = dcc.Slider(3, 15, 1, value=5, id="ma")
ticker_name = html.Div(
    dbc.FormFloating(
        [
            dbc.Input(type="text", id="ticker-name", debounce=True, value="AAPL"),
            dbc.Label("Ticker Name"),
            dbc.FormText("Enter Ticker Name"),
        ]
    )
)


def breaks(num):
    return [html.Br()] * num


sidebar = html.Div(
    [
        html.H2("Parameters", style=TEXT_STYLE),
        html.Hr(),
        dbc.Card(dbc.CardBody(ticker_name)),
        *breaks(1),
        dbc.Card(dbc.CardBody(ma_switch)),
        *breaks(1),
        dbc.Card(dbc.CardBody([html.P("Choose MA period"), slider])),
        *breaks(1),
    ],
    style=SIDEBAR_STYLE,
)
fig1 = dcc.Graph(id="fig1")

c_first_row = dbc.Row(
    [
        dbc.Col(dbc.Card(dbc.CardBody([timeframe, fig1]))),
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
        Input("ma-switch", "value"),
        Input("timeframe", "value"),
    ],
)
def refresh_fig1(name, i, smoothing, ma_sw, tf):
    start, end = datetime.now() + timedelta(hours=-48), datetime.now()
    df = get_data(name, start, end, tf)
    # df = prettify(data).iloc[i : 60 + i + smoothing, :]
    moving_average = (
        df.iloc[1:, :]
        .rolling(window=smoothing)
        .mean()
        .apply(lambda x: (x["o"] + x["h"] + x["l"] + x["c"]) / 4, axis=1)
    )
    fig1 = go.Figure(
        data=[
            go.Candlestick(
                x=df["t"],
                open=df["o"],
                high=df["h"],
                low=df["l"],
                close=df["c"],
                name="OHLC",
            )
        ]
    )
    fig1.update_layout(height=650, title=f"{name.upper()}")
    fig1.update_layout(
        yaxis=dict(autorange=True, fixedrange=False),
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=15, label="15m", step="minute", stepmode="backward"),
                        dict(count=60, label="1H", step="minute", stepmode="backward"),
                        dict(count=4, label="4H", step="hour", stepmode="backward"),
                        dict(count=24, label="24h", step="hour", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
    )
    if ma_sw:
        fig1.add_trace(
            go.Scatter(x=df["t"], y=moving_average, name=f"MA{smoothing}", mode="lines")
        )

    return fig1


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
