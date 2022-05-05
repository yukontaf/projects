import yfinance as yf
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc
from main import app

import time

prettify = lambda x: (
    pd.DataFrame(x.history(period="7d", interval="1m"))
    .sort_index(ascending=True)
    .reset_index()
)
