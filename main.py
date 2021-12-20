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

def check_main(pd_dataframe):
    try:
        sma8 = algorithms.sma(pd_dataframe, 8)
        current_rsi = algorithms.get_current_rsi(pd_dataframe)
        if pd_dataframe['trade_price'].iloc[-1] > sma8.iloc[-1] :
            return True
        return False
    except Exception as e:    
        print("raise error ", e)
        return False

def check_sub(pd_dataframe):
    try:
        point = 0
        current_pdf = pd_dataframe

        sma5 = algorithms.sma(current_pdf, 5)
        sma20 = algorithms.sma(current_pdf, 20)
        sma60 = algorithms.sma(current_pdf, 60)
        # 단기 골든 크로스 MA(5,20)
        if sma5.iloc[-1] > sma20.iloc[-1]:
            print('단기 골든 크로스 MA(5,20)')
            point += 1
        
        # 중기 골든 크로스 MA(20,60)
        if sma20.iloc[-1] > sma60.iloc[-1]:
            print('중기 골든 크로스 MA(20,60)')
            point += 1
            
        # 당일 거래 급증 종목(10일 평균 거래대비)
        obv, obv_ema = algorithms.get_obv(current_pdf, 10)
        if obv.iloc[-1] > obv_ema.iloc[-1]:
            print('당일 거래 급증 종목')
            point += 1
        
        # Stochastic slow(10,5,5) %K, %D 상향돌파
        if algorithms.is_stc_slow_good(pd_dataframe, 9, 3, 3) < 55:
            print('Stochastic slow(9,3,3) %K, %D 상향돌파')
            point += 1
        
        # MACD Osc(12,26,9) 0선 상향돌파
        if algorithms.macd_line_over_than_signal(pd_dataframe):
            print('MACD')
            point += 1
        
        # RSI(14,9) Signal선 상향돌파
        rsi9 = algorithms.rsi(current_pdf, 9)
        rsi14 = algorithms.rsi(current_pdf, 14)
        if rsi9.iloc[-1] > rsi14.iloc[-1]: 
            print('rsi')
            point += 1

        cci9 = algorithms.get_current_cci(current_pdf, 9)
        cci20 = algorithms.get_current_cci(current_pdf, 20)
        if cci9 > cci20 :
            print('cci')
            point += 1

        return point
    except Exception as e:    
        print("raise error ", e)
        return 0

def is_contains(name, target_list):
    for target in target_list:
        if name in target:
            return True
    return False
    
def buy_thread():
    global balance_list
    market_group = get_market_groups('KRW')
    store = Store()
    while True:
        try:
            buy_list = []
            balance_list = store.get_balance_list()
            for maket in market_group:
                coin = maket.get("market")

                print('buy check ' + coin)
                data_center = UpbitDataCenter(coin)
                point = check_sub(data_center.week_trader.data)
                current_rsi = algorithms.get_current_rsi(data_center.week_trader.data)
                if point >= 4 and current_rsi <= 70 and current_rsi >= 50:
                    sma8 = algorithms.sma(data_center.week_trader.data, 8)
                    margin = algorithms.get_margin(sma8.iloc[-1], data_center.week_trader.data['trade_price'].iloc[-1])
                    if sma8.iloc[-1] > data_center.week_trader.data['trade_price'].iloc[-1] : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : -' + str(round(margin,3)) ) 
                    print('buy')

            if len(buy_list) > 0:
                buy_list.append('========================================== day')

            for maket in market_group:
                coin = maket.get("market")

                print('buy check ' + coin)
                data_center = UpbitDataCenter(coin)
                point = check_sub(data_center.day_trader.data)
                current_rsi = algorithms.get_current_rsi(data_center.day_trader.data)
                if point >= 5 and current_rsi <= 58:
                    sma8 = algorithms.sma(data_center.day_trader.data, 8)
                    margin = algorithms.get_margin(sma8.iloc[-1], data_center.day_trader.data['trade_price'].iloc[-1])

                    temp_word = ' '
                    if is_contains(coin, buy_list):
                        temp_word = ' good parent'
                    else :
                        temp_word = ' ' 

                    if sma8.iloc[-1] > data_center.day_trader.data['trade_price'].iloc[-1] : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : -' + str(round(margin,3)) + temp_word) 
                    else : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : +' + str(round(margin,3)) + temp_word) 
                    print('buy')

            if len(buy_list) > 0:
                buy_list.append('========================================== minute240')

            for maket in market_group:
                coin = maket.get("market")
                print('buy check ' + coin)
                data_center = UpbitDataCenter(coin)
                point = check_sub(data_center.minute240_trader.data)
                current_rsi = algorithms.get_current_rsi(data_center.minute240_trader.data)
                if point >= 5 and current_rsi <= 58:
                    sma8 = algorithms.sma(data_center.minute240_trader.data, 8)
                    margin = algorithms.get_margin(sma8.iloc[-1], data_center.minute240_trader.data['trade_price'].iloc[-1])

                    temp_word = ''
                    if is_contains(coin, buy_list):
                        temp_word = ' good parent'
                    else :
                        temp_word = '' 

                    if sma8.iloc[-1] > data_center.minute240_trader.data['trade_price'].iloc[-1] : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : -' + str(round(margin,3)) + temp_word) 
                    else : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : +' + str(round(margin,3)) + temp_word) 
                    print('buy')

            if len(buy_list) > 0:
                buy_list.append('========================================== minute 30')

            for maket in market_group:
                coin = maket.get("market")
                print('buy check ' + coin)
                data_center = UpbitDataCenter(coin)
                point = check_sub(data_center.minute30_trader.data)
                current_rsi = algorithms.get_current_rsi(data_center.minute30_trader.data)
                if point >= 5 and current_rsi <= 58:
                    sma8 = algorithms.sma(data_center.minute30_trader.data, 8)

                    temp_word = ''
                    if is_contains(coin, buy_list):
                        temp_word = ' good parent'
                    else :
                        temp_word = '' 

                    margin = algorithms.get_margin(sma8.iloc[-1], data_center.minute30_trader.data['trade_price'].iloc[-1])
                    if sma8.iloc[-1] > data_center.minute30_trader.data['trade_price'].iloc[-1] : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : -' + str(round(margin,3)) + temp_word) 
                    else : 
                        buy_list.append(coin + ' ' + str(point) + ' margin : +' + str(round(margin,3)) + temp_word) 
                    print('buy')

            if len(buy_list) > 0:
                current_result = '\r\n'.join(buy_list)
                send_mail(current_result, "check result")
                    
        except Exception as e:    
            print("raise error ", e)
        
        time.sleep(1300)

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
                current_price = data_center.minute30_trader.data['trade_price'].iloc[-1]

                ha_candle_df = algorithms.heikin_ashi(data_center.minute30_trader.data)
                current_price = data_center.minute30_trader.data['trade_price'].iloc[-1]
                store = Store()

                # if ha_candle_df['close'].iloc[-2] < ha_candle_df['open'].iloc[-2] and \
                #    ha_candle_df['close'].iloc[-1] < ha_candle_df['low'].iloc[-2] :
                #     store.sell(market_name, coin.balance, current_price)      

            except Exception as e:    
                print("raise error ", e)
                
        time.sleep(60)

def main():
    th1 = Thread(target=buy_thread, args=())
    #th2 = Thread(target=sell_thread, args=())

    th1.start()
    #th2.start()

    th1.join()
    #th2.join()
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
