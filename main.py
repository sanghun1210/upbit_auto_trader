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
from threading import Thread

balance_name_list = []
balance_list = []

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


def check_buy(coin_name, pd_dataframe):
    #이제 5분보을 바라보고 골든크로스를 구매해야 한다.
    #골든 크로스를 찾는다.
    current_price = pd_dataframe['trade_price'].iloc[-1]

    if algorithms.macd_cross(pd_dataframe) and \
        algorithms.is_stc_slow_good(pd_dataframe):
        store = Store()
        store.buy(coin_name, float(15000/ current_price), current_price)
        return True
    return False
    
def get_my_coin_list():
    my_list = []
    my_list.append('KRW-AERGO')
    my_list.append('KRW-XTZ')
    my_list.append('KRW-ADA')
    my_list.append('KRW-ATOM')
    my_list.append('KRW-WAVES')
    my_list.append('KRW-XEC')
    my_list.append('KRW-LINK')
    my_list.append('KRW-SRM')
    my_list.append('KRW-CRO')
    my_list.append('KRW-AXS')
    my_list.append('KRW-KAVA')
    my_list.append('KRW-THETA')
    my_list.append('KRW-HBAR')
    my_list.append('KRW-OMG')
    my_list.append('KRW-GAS')
    my_list.append('KRW-MTL')
    my_list.append('KRW-DOT') 
    my_list.append('KRW-MLK')
    my_list.append('KRW-FCT2')
    return my_list

#60분봉의 macd라인이 위에 있어야 한다.
#5분봉의 골든크로스 지점 매수
#5분봉의 데드크로스 지점 매도
def buy_thread():
    global balance_list
    market_group = get_market_groups('KRW')
    store = Store()
    while True:
        try:
            balance_list = store.get_balance_list()
            coin_list = get_my_coin_list()
            for maket in market_group:
                coin = maket.get("market")
                is_aleady_have = False

                for balance in balance_list:
                    if balance.currency == coin:
                        is_aleady_have = True

                if is_aleady_have or len(balance_list) > 5:
                    continue

                print('buy check ' + coin)
                data_center = UpbitDataCenter(coin)
                ha_candle_df = algorithms.heikin_ashi(data_center.minute240_trader.data)
                current_price = data_center.minute240_trader.data['trade_price'].iloc[-1]

                if ha_candle_df['close'].iloc[-1] > algorithms.get_current_sma(data_center.minute240_trader.data, 9) and \
                    ha_candle_df['close'].iloc[-2] > ha_candle_df['open'].iloc[-2] and algorithms.get_current_rsi(data_center.minute240_trader.data) < 61:
                    if ha_candle_df['close'].iloc[-3] < ha_candle_df['open'].iloc[-3] or ha_candle_df['close'].iloc[-4] < ha_candle_df['open'].iloc[-4]:
                        store = Store()
                        store.buy(coin, float(15000/ current_price), current_price)
                        balance_list = store.get_balance_list()
                    
                
                # algorithms.plot_trend(tr)
                # if algorithms.obv_is_good(data_center.minute60_trader.data):
                #     if check_buy(coin, data_center.minute10_trader.data):
                #         balance_list = store.get_balance_list()
                        
                    

                # if algorithms.macd_line_over_than_signal(data_center.day_trader.data) and \
                #     algorithms.obv_is_good(data_center.day_trader.data):
                #     if check_buy(coin, data_center.minute240_trader.data) : 
                #         balance_list = store.get_balance_list()
                    
                # elif algorithms.macd_line_over_than_signal(data_center.minute240_trader.data) and \
                #     algorithms.obv_is_good(data_center.minute240_trader.data):
                #     if check_buy(coin, data_center.minute30_trader.data) : 
                #         balance_list = store.get_balance_list()    
                    
        except Exception as e:    
            print("raise error ", e)
        
        time.sleep(30)

def sell_thread():
    store = Store()
    while True:   
        current_balance_list = store.get_balance_list()
        for coin in current_balance_list:
            try:
                market_name = coin.currency  
                if market_name == "KRW-KRW" or market_name == "KRW-IOTX":
                    continue
                print('sell check ' + market_name)
                data_center = UpbitDataCenter(market_name) 
                current_price = data_center.minute60_trader.data['trade_price'].iloc[-1]

                ha_candle_df = algorithms.heikin_ashi(data_center.minute240_trader.data)
                current_price = data_center.minute240_trader.data['trade_price'].iloc[-1]
                store = Store()

                if ha_candle_df['close'].iloc[-1] < algorithms.get_current_sma(data_center.minute240_trader.data, 9) :
                    store = Store()
                    store.sell(market_name, coin.balance, current_price)      

            except Exception as e:    
                print("raise error ", e)
                
        time.sleep(60)

def main():
    th1 = Thread(target=buy_thread, args=())
    th2 = Thread(target=sell_thread, args=())

    th1.start()
    th2.start()

    th1.join()
    th2.join()
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
