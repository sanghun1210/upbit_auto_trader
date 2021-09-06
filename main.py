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

def get_margin(self, a, b):
        ma = 0
        if a > b:
            ma = ((a - b) / a) * 100
        else : 
            ma = ((b - a) / b) * 100
        return ma

def get_balance(balance_list, market_name):
    for balance in balance_list:
        if balance.currency == market_name:
            return balance
    return None

def is_nice_main_trader(trader):
    current_price = trader.data['trade_price'].iloc[-1]
    # print(algorithms.get_current_sma(trader.data, 8))
    # print(algorithms.get_current_rsi(trader.data))

    # if current_price < algorithms.get_current_sma(trader.data, 10):
    #     return False
    
    if current_price >= algorithms.get_current_sma(trader.data, 10) \
        and algorithms.get_current_rsi(trader.data) > 50:
        return True
    return False
        

def is_nice_trader(trader, max_bol_width, add_msg):
    add_msg[0] = ''
    current_price = trader.data['trade_price'].iloc[-1]
    current_rsi = algorithms.get_current_rsi(trader.data) 
    #mos = trader.get_momentum_list()
    
    if algorithms.bbands_width(trader.data,8) > max_bol_width:
        return False

    if current_rsi >= 48 and current_rsi <= 70 and algorithms.macd_line_over_than_signal(trader.data):
        if current_price >= algorithms.get_current_sma(trader.data, 8):
            add_msg[0] = ' good_pattern'
            return True

    # if algorithms.bbands_is_low_touch(trader.data, 8):
    #     add_msg[0] = ' low_pattern'
    #     return True

    return False

def main():
    while True:
        try:
            coin_list = get_market_groups('KRW')
            store = Store()
            balance_list = store.get_balance_list()
            buy_list = []
            for coin in coin_list:
                is_buy=False
                coin_name = coin.get("market")
                data_center = UpbitDataCenter(coin_name)
                print(coin_name)

                add_msg = []
                add_msg.append('')

                current_price = data_center.day_trader.data['trade_price'].iloc[-1]
                if current_price < algorithms.get_current_sma(data_center.day_trader.data, 5):
                    continue

                if is_nice_main_trader(data_center.week_trader) and \
                    is_nice_trader(data_center.day_trader, 15, add_msg):
                    coin_name = coin_name + ' day!' + add_msg[0]
                    print(coin_name)
                    is_buy = True


                if is_nice_main_trader(data_center.day_trader) and \
                    is_nice_trader(data_center.minute240_trader, 10, add_msg):
                    coin_name = coin_name + ' 240m! ' + add_msg[0]
                    print(coin_name)
                    is_buy = True

                if is_nice_main_trader(data_center.minute240_trader) and \
                    is_nice_trader(data_center.minute30_trader, 3.5, add_msg):
                    coin_name = coin_name + ' 30m! ' + add_msg[0]
                    print(coin_name)
                    is_buy = True

                # if is_nice_main_trader(data_center.minute60_trader) and \
                #     is_nice_trader(data_center.minute10_trader, 2, add_msg):
                #     coin_name = coin_name + ' 10m! ' + add_msg[0]
                #     print(coin_name)
                #     is_buy = True

                

                # if is_nice_main_trader(data_center.day_trader) and \
                #     is_nice_trader(data_center.minute240_trader, 11, add_msg):
                #     coin_name = coin_name + ' 240m!' + add_msg[0]
                #     print('240m!')
                #     is_buy = True

                # if is_nice_main_trader(data_center.week_trader) and \
                #     is_nice_trader(data_center.day_trader, 13, add_msg):
                #     coin_name = coin_name + ' day!' + add_msg[0]
                #     print('240m!')
                #     is_buy = True

                if is_buy :
                    buy_list.append(coin_name)

            if len(buy_list) > 0:
                current_result = '\r\n'.join(buy_list)
                send_mail(current_result, "check result")
            time.sleep(800)

        except Exception as e:    
            print("raise error ", e)
if __name__ == "__main__":
    # execute only if run as a script
    main()
