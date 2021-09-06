
import json
import time
import requests
from .base_trader import *

import os
import sys

from .candle import *


def get_week_candle_list(market_name, count) :
    str_list = []
    str_list.append("https://api.upbit.com/v1/candles/weeks")
    url =  ''.join(str_list)
    querystring = {"market": market_name, "count": count}
    response = requests.request("GET", url, params=querystring)
    time.sleep(0.1)
    return response.json()


class WeekTrader(BaseTrader):
    def __init__(self, market_name, count):
        super().__init__(market_name)
        self.json_candles = get_week_candle_list(market_name, count)
        self.data = pd.DataFrame(self.json_candles)
        self.data = self.data[::-1].reset_index(drop=True)

    


