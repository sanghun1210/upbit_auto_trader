import numpy as np
import pandas as pd
import algorithms.obv


def stc_slow_plot(goog_data, N=14, M=5, T=5) :
    L = goog_data["low_price"].rolling(window=N).min()
    H = goog_data["high_price"].rolling(window=N).max()

    fast_k = ((goog_data["trade_price"] - L) / (H - L)) * 100
    slow_k = fast_k.ewm(span=M).mean()
    slow_d = slow_k.ewm(span=T).mean()

    goog_data['signal'] = pd.Series(np.zeros(len(goog_data)))
    goog_data['position'] = pd.Series(np.zeros(len(goog_data)))

    goog_data = algorithms.obv_with_ema(goog_data)

    

    for i in range(1,len(goog_data)):
        if slow_d.iloc[i] < 30 and slow_k.iloc[i] > slow_d.iloc[i]  : 
            goog_data['signal'].iloc[i] = 1
            
        elif slow_k.iloc[i] > 50 and  slow_k.iloc[i] < slow_d.iloc[i] : 
            goog_data['signal'].iloc[i] = 0

    # goog_data['signal'][0:] =\
    #     np.where((slow_d[0:] < 30 and slow_k[0:] > slow_d[0:]), 1.0, 0.0)
    goog_data['orders'] = goog_data['signal'].diff()

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(211, ylabel='Google price in $')
    goog_data["trade_price"].plot(ax=ax1, color='g', lw=.5)
    ax1.plot(goog_data.loc[goog_data.orders== 1.0].index,
            goog_data["trade_price"][goog_data.orders == 1.0],
            '^', markersize=7, color='k')

    ax1.plot(goog_data.loc[goog_data.orders== -1.0].index,
            goog_data["trade_price"][goog_data.orders == -1.0],
            'v', markersize=7, color='k')


    # ax2 = fig.add_subplot(312, ylabel='MACD')
    # slow_k.plot(ax=ax2, color='black', lw=2., legend=True)
    # slow_d.plot(ax=ax2, color='g', lw=2., legend=True)

    # plt.legend(["Price","Short mavg","Long mavg","Buy","Sell"])
    plt.title("stc")

    plt.show()

def stc_slow(data, N=9, M=3, T=3) :
    L = data["low_price"].rolling(window=N).min()
    H = data["high_price"].rolling(window=N).max()

    fast_k = ((data["trade_price"] - L) / (H - L)) * 100
    slow_k = fast_k.ewm(span=M).mean()
    slow_d = slow_k.ewm(span=T).mean()
    return slow_k, slow_d



def is_stc_slow_good(data, N=9, M=3, T=3) :
    L = data["low_price"].rolling(window=N).min()
    H = data["high_price"].rolling(window=N).max()

    fast_k = ((data["trade_price"] - L) / (H - L)) * 100
    slow_k = fast_k.ewm(span=M).mean()
    slow_d = slow_k.ewm(span=T).mean()

    if slow_k.iloc[-1] > slow_d.iloc[-1]:
        return slow_d.iloc[-1]
    return 100

def is_stc_slow_bad(data, N=9, M=3, T=3) :
    L = data["low_price"].rolling(window=N).min()
    H = data["high_price"].rolling(window=N).max()

    fast_k = ((data["trade_price"] - L) / (H - L)) * 100
    slow_k = fast_k.ewm(span=M).mean()
    slow_d = slow_k.ewm(span=T).mean()

    return slow_k.iloc[-1] < slow_d.iloc[-1]
