import pandas as pd
from pandas_datareader import data
import numpy as np

def obv(pd_dataframe):
    # obv가 저장될 pandas series를 생성
    pd_dataframe['obv'] = pd.Series(index=pd_dataframe['trade_price'].index)
    pd_dataframe['obv'].iloc[0] = pd_dataframe['candle_acc_trade_volume'].iloc[0]
    
    # OBV 산출공식을 구현
    # pd.Series 구조를 연산에 직접 사용
    for i in range(1,len(pd_dataframe)):
        if pd_dataframe['trade_price'].iloc[i] > pd_dataframe['trade_price'].iloc[i-1] : 
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] + pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
        elif pd_dataframe['trade_price'].iloc[i] < pd_dataframe['trade_price'].iloc[i-1] :
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] - pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
        else:
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1]

    return pd_dataframe['obv']

def get_margin(a, b):
        ma = 0
        if a > b:
            ma = ((a - b) / a) * 100
        else : 
            ma = ((b - a) / b) * 100
        return ma


# def obv_is_good_by_margin(pd_dataframe, margin = 0, logger):
#     # obv가 저장될 pandas series를 생성
#     pd_dataframe['obv'] = pd.Series(index=pd_dataframe['trade_price'].index)
#     pd_dataframe['obv'].iloc[0] = pd_dataframe['candle_acc_trade_volume'].iloc[0]
    
#     # OBV 산출공식을 구현
#     # pd.Series 구조를 연산에 직접 사용
#     for i in range(1,len(pd_dataframe)):
#         if pd_dataframe['trade_price'].iloc[i] > pd_dataframe['trade_price'].iloc[i-1] : 
#             pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] + pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
#         elif pd_dataframe['trade_price'].iloc[i] < pd_dataframe['trade_price'].iloc[i-1] :
#             pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] - pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
#         else:
#             pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1]

#     pd_dataframe['obv_ema'] = pd_dataframe['obv'].ewm(com=9).mean()

#     # import matplotlib.pyplot as plt

#     # fig = plt.figure()
#     # ax1 = fig.add_subplot(111, ylabel='Google price in $')
#     # pd_dataframe['obv'].plot(ax=ax1, color='g', lw=2., legend=True)
#     # pd_dataframe['obv_ema'] .plot(ax=ax1, color='b', lw=2., legend=True)
#     # plt.show()

#     is_obv_good = pd_dataframe['obv'].iloc[-1] > pd_dataframe['obv_ema'].iloc[-1]
#     if is_obv_good :
#         if margin > 0:
#             print('30 magin : ' + str(abs(get_margin(pd_dataframe['obv'].iloc[-1], pd_dataframe['obv_ema'].iloc[-1]) )))
#             return abs(get_margin(pd_dataframe['obv'].iloc[-1], pd_dataframe['obv_ema'].iloc[-1])) > margin
#         else :
#             return True
#     return False
    

def obv_is_good(pd_dataframe):
    # obv가 저장될 pandas series를 생성
    goog_data = pd_dataframe
    pd_dataframe['obv'] = pd.Series(index=pd_dataframe['trade_price'].index)
    pd_dataframe['obv'].iloc[0] = pd_dataframe['candle_acc_trade_volume'].iloc[0]
    
    # OBV 산출공식을 구현
    # pd.Series 구조를 연산에 직접 사용
    for i in range(1,len(pd_dataframe)):
        if pd_dataframe['trade_price'].iloc[i] > pd_dataframe['trade_price'].iloc[i-1] : 
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] + pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
        elif pd_dataframe['trade_price'].iloc[i] < pd_dataframe['trade_price'].iloc[i-1] :
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] - pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
        else:
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1]

    pd_dataframe['obv_ema'] = pd_dataframe['obv'].ewm(com=12).mean()

    # pd_dataframe['signal'] = pd.Series(np.zeros(len(goog_data)))
    # pd_dataframe['position'] = pd.Series(np.zeros(len(goog_data)))

    # pd_dataframe['signal'][0:] =\
    #     np.where(pd_dataframe['obv'][0:] > pd_dataframe['obv_ema'][0:], 1.0, 0.0)
    # pd_dataframe['orders'] = pd_dataframe['signal'].diff()

    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax1 = fig.add_subplot(211, ylabel='Google price in $')
    # goog_data["trade_price"].plot(ax=ax1, color='g', lw=.5)
    # ax1.plot(goog_data.loc[goog_data.orders== 1.0].index,
    #         goog_data["trade_price"][goog_data.orders == 1.0],
    #         '^', markersize=7, color='k')

    # ax1.plot(goog_data.loc[goog_data.orders== -1.0].index,
    #         goog_data["trade_price"][goog_data.orders == -1.0],
    #         'v', markersize=7, color='k')


    # ax2 = fig.add_subplot(312, ylabel='MACD')
    # pd_dataframe['obv'].plot(ax=ax2, color='black', lw=2., legend=True)
    # pd_dataframe['obv_ema'].plot(ax=ax2, color='g', lw=2., legend=True)

    # plt.legend(["Price","Short mavg","Long mavg","Buy","Sell"])
    # plt.title("Double Moving Average Trading Strategy")

    # plt.show()
    return pd_dataframe['obv'].iloc[-1] > pd_dataframe['obv_ema'].iloc[-1]

def obv_with_ema(pd_dataframe):
    # obv가 저장될 pandas series를 생성
    goog_data = pd_dataframe
    pd_dataframe['obv'] = pd.Series(index=pd_dataframe['trade_price'].index)
    pd_dataframe['obv'].iloc[0] = pd_dataframe['candle_acc_trade_volume'].iloc[0]
    
    # OBV 산출공식을 구현
    # pd.Series 구조를 연산에 직접 사용
    for i in range(1,len(pd_dataframe)):
        if pd_dataframe['trade_price'].iloc[i] > pd_dataframe['trade_price'].iloc[i-1] : 
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] + pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
        elif pd_dataframe['trade_price'].iloc[i] < pd_dataframe['trade_price'].iloc[i-1] :
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1] - pd_dataframe['candle_acc_trade_volume'].iloc[i]
            
        else:
            pd_dataframe['obv'].iloc[i] = pd_dataframe['obv'].iloc[i-1]

    pd_dataframe['obv_ema'] = pd_dataframe['obv'].ewm(com=10).mean()

    # plt.show()
    return pd_dataframe