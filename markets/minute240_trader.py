
import json
import time
import requests
from .base_trader import *

import os
import sys
from .candle import *
from .calcualtor import *

import pandas as pd

def get_candle_list(market_name, minute_unit, count) :
    str_list = []
    str_list.append("https://api.upbit.com/v1/candles/minutes/")
    str_list.append(str(minute_unit))
    url =  ''.join(str_list)
    querystring = {"market": market_name, "count": count}
    response = requests.request("GET", url, params=querystring)
    time.sleep(0.1)
    return response.json()


class Minute240Trader(BaseTrader):
    def __init__(self, market_name, count, src_logger):
        super().__init__(market_name, src_logger)
        json_candles = get_candle_list(market_name, 240, count)
        

        import numpy as np

        goog_data_signal = pd.DataFrame(json_candles)
        goog_data_signal = goog_data_signal[::-1].reset_index(drop=True)
        goog_data_signal['daily_difference'] = goog_data_signal['trade_price'].diff()
        goog_data_signal['signal'] = 0.0
        goog_data_signal['signal'][:] = np.where(goog_data_signal['daily_difference'][:] > 0, 1.0, 0.0)
        goog_data_signal['positions'] = goog_data_signal['signal'].diff()

        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Google price in $')
        goog_data_signal['trade_price'].plot(ax=ax1, color='r', lw=2.)

        ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,
         goog_data_signal.trade_price[goog_data_signal.positions == 1.0],
         '^', markersize=5, color='m')

        ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
         goog_data_signal.trade_price[goog_data_signal.positions == -1.0],
         'v', markersize=5, color='k')

        plt.show()


        # self.create_candle_list_from_json(json_candles)
        # self.trader_name = 'Minute240Trader'
        # self.cross_margin = 0.8

    








        

        


    




