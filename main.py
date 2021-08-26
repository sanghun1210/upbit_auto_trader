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
        
        for market in market_group:
            market_name = market.get("market")
            data_center = UpbitDataCenter(market_name)
            print(market_name)
            algorithms.macd(data_center.minute240_trader.data)
            # ts = algorithms.double_moving_average(data_center.minute60_trader.data,20,100)
            # algorithms.plot_double_moving_average(ts, data_center.minute60_trader.data)


    except Exception as e:    
        print("raise error ", e)
if __name__ == "__main__":
    # execute only if run as a script
    main()
