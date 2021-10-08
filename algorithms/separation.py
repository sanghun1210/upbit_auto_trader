import pandas as pd

from pandas_datareader import data
from algorithms import get_current_sma


def get_current_separation(df, period): 
    sma = get_current_sma(df, period)
    df['trade_price'].iloc[-1]
