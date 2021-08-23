
import json
import time
import requests
from .base_trader import *

import os
import sys



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
        self.json_candles = get_candle_list(market_name, 240, count)

        self.market_data = pd.DataFrame(self.json_candles)
        self.market_data = self.market_data[::-1].reset_index(drop=True)
        self.market_data['daily_difference'] = self.market_data['trade_price'].diff()
        # self.market_data['signal'] = 0.0
        # self.market_data['signal'][:] = np.where(self.market_data['daily_difference'][:] > 0, 1.0, 0.0)
        # self.market_data['positions'] = self.market_data['signal'].diff()

        self.trading_support_resistance(self.market_data)

        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Google price in $')
        self.market_data['sup'].plot(ax=ax1, color='g', lw=2.)
        self.market_data['res'].plot(ax=ax1, color='b', lw=2.)
        self.market_data['trade_price'].plot(ax=ax1, color='r', lw=2.)

        ax1.plot(self.market_data.loc[self.market_data.positions == 1.0].index,
         self.market_data.trade_price[self.market_data.positions == 1.0],
         'v', markersize=7, color='k', label='sell')

        ax1.plot(self.market_data.loc[self.market_data.positions == -1.0].index,
         self.market_data.trade_price[self.market_data.positions == -1.0],
         '^', markersize=7, color='k', label='buy')

        plt.show()







        

        


    




