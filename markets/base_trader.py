
import json
import time
import requests

import os
import sys
from . import *

from .candle import *
from .calcualtor import *
from enum import Enum
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BaseTrader():
    def __init__(self, market_name, src_logger):
        self.market_name = market_name
        self.logger = src_logger
        self.market_data = None
        self.json_candles = None

    #RSI계산 함수
    def rsi_calculate(self, l, n, sample_number): #l = price_list, n = rsi_number
        
        diff=[]
        au=[]
        ad=[]

        if len(l) != sample_number: #url call error
            return -1 
        for i in range(len(l)-1):
            diff.append(l[i+1]-l[i]) #price difference
        
        au = pd.Series(diff) #list to series
        ad = pd.Series(diff)

        au[au<0] = 0 #remove ad
        ad[ad>0] = 0 #remove au

        _gain = au.ewm(com = n, min_periods = sample_number -1).mean() #Exponentially weighted average
        _loss = ad.abs().ewm(com = n, min_periods = sample_number -1).mean()
        RS = _gain/_loss

        rsi = 100-(100 / (1+RS.iloc[-1]))

        return rsi

    def trading_support_resistance(self, data, bin_width=20):
        data['sup_tolerance'] = pd.Series(np.zeros(len(data)))
        data['res_tolerance'] = pd.Series(np.zeros(len(data)))
        data['sup_count'] = pd.Series(np.zeros(len(data)))
        data['res_count'] = pd.Series(np.zeros(len(data)))
        data['sup'] = pd.Series(np.zeros(len(data)))
        data['res'] = pd.Series(np.zeros(len(data)))

        data['positions'] = pd.Series(np.zeros(len(data)))
        data['signal'] = pd.Series(np.zeros(len(data)))
        in_support = 0
        in_resistance = 0
        for x in range((bin_width - 1) + bin_width, len(data)):
            data_section = data[x - bin_width:x + 1]
            support_level=min(data_section['trade_price'])
            resistance_level = max(data_section['trade_price'])
            range_level=resistance_level - support_level
            data['res'][x]=resistance_level
            data['sup'][x]=support_level
            data['sup_tolerance'][x]=support_level + 0.2 * range_level
            data['res_tolerance'][x]=resistance_level - 0.2 * range_level

            if data['trade_price'][x]>=data['res_tolerance'][x] and \
                data['trade_price'][x] <= data['res'][x]:
                in_resistance += 1
                data['res_count'][x] = in_resistance
            elif data['trade_price'][x] <= data['sup_tolerance'][x] and \
                data['trade_price'][x] >= data['sup'][x]:
                in_support += 1
                data['sup_count'][x] = in_support
            else:
                in_support=0
                in_resistance=0

            if in_resistance>2:
                data['signal'][x]=1
            elif in_support>2:
                data['signal'][x]=0
            else:
                data['signal'][x] = data['signal'][x-1]

        data['positions'] = data['signal'].diff()

    def double_moving_average(self, short_window, long_window):
        self.market_data = pd.DataFrame(self.json_candles)
        self.market_data = self.market_data[::-1].reset_index(drop=True)
        
        self.market_data['signal'] = 0.0
        self.market_data['short_mavg'] = financial_data['Close'].\
            rolling(window=short_window,
                    min_periods=1, center=False).mean()
        signals['long_mavg'] = financial_data['Close'].\
            rolling(window=long_window,
                    min_periods=1, center=False).mean()
        signals['signal'][short_window:] =\
            np.where(signals['short_mavg'][short_window:]
                                                    > signals['long_mavg'][short_window:], 1.0, 0.0)
        signals['orders'] = signals['signal'].diff()
        return signals





        



        



        


        






    