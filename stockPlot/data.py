import yfinance as yf
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc
from main import app
import requests
from datetime import datetime
import time

prettify = lambda x: (
    pd.DataFrame(x.history(period="7d", interval="1m"))
    .sort_index(ascending=True)
    .reset_index()
)


def get_data(ticker, start, end, tf):
    start, end, ticker = (
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        ticker.upper(),
    )
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{tf}/{start}/{end}?apiKey=03rMBckAiQMVjQpKTxWJdHRrtrn1Ytmm"
    ans = requests.get(url).json()
    ans = pd.DataFrame.from_dict(ans["results"])
    ans["t"] = ans["t"].apply(lambda x: pd.to_datetime(x, unit="ms"))

    return ans.reset_index()
