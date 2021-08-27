from store import Store
import requests
import json
import time
from mail import *
import datetime

from traders import *
from upbit_data_center import UpbitDataCenter
import logging
import algorithms

def get_markets_all() : 
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails":"false"}
    response = requests.request("GET", url, params=querystring)
    return response.json()

def get_market_groups(market_group_name) :
    json_markets = get_markets_all()
    selected_markets = []
    for json_market in json_markets:
        if market_group_name in json_market.get("market") :
            selected_markets.append(json_market)
    return selected_markets

def main():
    try:
        market_group = get_market_groups('KRW')

        store = Store()
        balance_list = store.get_balance_list()

        balance_name_list = []
        for balance in balance_list:
            balance_name_list.append(balance.currency)
        
        for market in market_group:
            market_name = market.get("market")
            data_center = UpbitDataCenter(market_name)
            print(market_name)
            # if market_name == 'KRW-IQ':
            #x = algorithms.get_stddev(data_center.minute60_trader.data,20)
        
            #algorithms.volatility_trend_following(data_center.minute60_trader.data, x)
            #algorithms.bbands(data_center.minute10_trader.data)

            if market_name == 'KRW-REP' or market_name == 'KRW-STX':
                continue

            if algorithms.bbands_is_low_touch(data_center.minute10_trader.data):
                # 구매
                if market_name in balance_name_list:
                    print('is_aleady_have')
                else:
                    print('buy')
                    store.buy(market_name, 8000)
                    balance_list = store.get_balance_list()
                    balance_name_list = []
                    for balance in balance_list:
                        balance_name_list.append(balance.currency)


            if algorithms.bbands_is_middle_touch(data_center.minute10_trader.data):
                if market_name in balance_name_list:
                    print('sell')
                    store.sell(market_name, 8000)
                    balance_list = store.get_balance_list()
                    balance_name_list = []
                    for balance in balance_list:
                        balance_name_list.append(balance.currency)
                else:
                    print('no')
                   

            #ts = algorithms.double_moving_average(data_center.minute10_trader.data,5,20)
            #algorithms.plot_double_moving_average(ts, data_center.minute10_trader.data)


    except Exception as e:    
        print("raise error ", e)
if __name__ == "__main__":
    # execute only if run as a script
    main()
