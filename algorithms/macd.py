import pandas as pd
import numpy as np
import algorithms.obv
import algorithms.macd

from pandas_datareader import data

def get_margin(a, b):
        ma = 0
        if a > b:
            ma = ((a - b) / a) * 100
        else : 
            ma = ((b - a) / b) * 100
        return ma

# def macd(df, period1, period2, period3): # default MACD period values are: period1 = 26, period2 = 12, period3 = 9.
#     df['ema1'] = df['trade_price'].ewm(span=period1, adjust=False).mean()
#     df['ema2'] = df['trade_price'].ewm(span=period2, adjust=False).mean()
#     df['macd_line'] = df['ema1'] - df['ema2']
#     df['macd_signal'] = df['macd_line'].ewm(span=period3, adjust=False).mean()
#     df['histogram'] = df['macd_line']  - df['macd_signal']
#     return df

# def macd_cross(pd_dataframe):
#     df = macd(pd_dataframe, 9, 16, 6)
#     df['signal'] = np.where(df['macd_line'] >  df['macd_signal'], 1.0, 0.0)
#     df['orders'] = df['signal'].diff()
#     return df['orders'].iloc[-1] > 0

# def macd_line_over_than_signal(pd_dataframe, short, long, signal):
#     df = macd(pd_dataframe, short, long, signal)
#     return df['histogram'].iloc[-1] >= 0

def macd_plot(goog_data):
    close = goog_data['trade_price']
    num_periods_fast = 6 # fast EMA time period
    K_fast = 2 / (num_periods_fast + 1) # fast EMA smoothing factor
    ema_fast = 0
    num_periods_slow = 19 # slow EMA time period
    K_slow = 2 / (num_periods_slow + 1) # slow EMA smoothing factor
    ema_slow = 0
    num_periods_macd = 6 # MACD EMA time period
    K_macd = 2 / (num_periods_macd + 1) # MACD EMA smoothing factor
    ema_macd = 0

    ema_fast_values = [] # track fast EMA values for visualization purposes
    ema_slow_values = [] # track slow EMA values for visualization purposes
    macd_values = [] # track MACD values for visualization purposes
    macd_signal_values = [] # MACD EMA values tracker
    macd_historgram_values = [] # MACD - MACD-EMA
    for close_price in close:
        if (ema_fast == 0): # first observation
            ema_fast = close_price
            ema_slow = close_price
        else:
            ema_fast = (close_price - ema_fast) * K_fast + ema_fast
            ema_slow = (close_price - ema_slow) * K_slow + ema_slow

        ema_fast_values.append(ema_fast)
        ema_slow_values.append(ema_slow)

        macd = ema_fast - ema_slow # MACD is fast_MA - slow_EMA
        if ema_macd == 0:
            ema_macd = macd
        else:
            ema_macd = (macd - ema_macd) * K_macd + ema_macd # signal is EMA of MACD values

        macd_values.append(macd)
        macd_signal_values.append(ema_macd)
        macd_historgram_values.append(macd - ema_macd)

    goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
    goog_data = goog_data.assign(FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=goog_data.index))
    goog_data = goog_data.assign(SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=goog_data.index))
    goog_data = goog_data.assign(MovingAverageConvergenceDivergence=pd.Series(macd_values, index=goog_data.index))
    goog_data = goog_data.assign(Exponential20DayMovingAverageOfMACD=pd.Series(macd_signal_values, index=goog_data.index))
    goog_data = goog_data.assign(MACDHistorgram=pd.Series(macd_historgram_values, index=goog_data.index))

    close_price = goog_data['ClosePrice']
    ema_f = goog_data['FastExponential10DayMovingAverage']
    ema_s = goog_data['SlowExponential40DayMovingAverage']
    macd = goog_data['MovingAverageConvergenceDivergence']
    ema_macd = goog_data['Exponential20DayMovingAverageOfMACD']
    macd_histogram = goog_data['MACDHistorgram']
    goog_data['signal'] = pd.Series(np.zeros(len(goog_data)))
    goog_data['position'] = pd.Series(np.zeros(len(goog_data)))

    # goog_data['signal'][0:] =\
    #     np.where(macd[0:] > ema_macd[0:], 1.0, 0.0)
    # goog_data['orders'] = goog_data['signal'].diff()

    for i in range(1,len(goog_data)):
        if macd.iloc[i] >  ema_macd.iloc[i] and  ema_macd.iloc[i] >=0 : 
            goog_data['signal'].iloc[i] = 1
            
        else : 
            goog_data['signal'].iloc[i] = 0

    goog_data['orders'] = goog_data['signal'].diff()
    print(goog_data)

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Google price in $')
    goog_data["trade_price"].plot(ax=ax1, color='g', lw=.5)
    ax1.plot(goog_data.loc[goog_data.orders== 1.0].index,
            goog_data["trade_price"][goog_data.orders == 1.0],
            '^', markersize=7, color='k')

    ax1.plot(goog_data.loc[goog_data.orders== -1.0].index,
            goog_data["trade_price"][goog_data.orders == -1.0],
            'v', markersize=7, color='k')


    # ax2 = fig.add_subplot(312, ylabel='MACD')
    # macd.plot(ax=ax2, color='black', lw=2., legend=True)
    # ema_macd.plot(ax=ax2, color='g', lw=2., legend=True)

    plt.legend(["Price","Short mavg","Long mavg","Buy","Sell"])
    plt.title("Double Moving Average Trading Strategy")

    plt.show()

    # fig = plt.figure()
    # ax1 = fig.add_subplot(311, ylabel='Google price in $')
    # close_price.plot(ax=ax1, color='g', lw=2., legend=True)
    # ema_f.plot(ax=ax1, color='b', lw=2., legend=True)
    # ema_s.plot(ax=ax1, color='r', lw=2., legend=True)
    # ax2 = fig.add_subplot(312, ylabel='MACD')
    # macd.plot(ax=ax2, color='black', lw=2., legend=True)
    # ema_macd.plot(ax=ax2, color='g', lw=2., legend=True)
    # ax3 = fig.add_subplot(313, ylabel='MACD')
    # macd_histogram.plot(ax=ax3, color='r', kind='bar', legend=True, use_index=False)
    # plt.show()


def macd(goog_data):
    close = goog_data['trade_price']
    num_periods_fast = 12 # fast EMA time period
    K_fast = 2 / (num_periods_fast + 1) # fast EMA smoothing factor
    ema_fast = 0
    num_periods_slow = 26 # slow EMA time period
    K_slow = 2 / (num_periods_slow + 1) # slow EMA smoothing factor
    ema_slow = 0
    num_periods_macd = 9 # MACD EMA time period
    K_macd = 2 / (num_periods_macd + 1) # MACD EMA smoothing factor
    ema_macd = 0

    ema_fast_values = [] # track fast EMA values for visualization purposes
    ema_slow_values = [] # track slow EMA values for visualization purposes
    macd_values = [] # track MACD values for visualization purposes
    macd_signal_values = [] # MACD EMA values tracker
    macd_historgram_values = [] # MACD - MACD-EMA
    for close_price in close:
        if (ema_fast == 0): # first observation
            ema_fast = close_price
            ema_slow = close_price
        else:
            ema_fast = (close_price - ema_fast) * K_fast + ema_fast
            ema_slow = (close_price - ema_slow) * K_slow + ema_slow

        ema_fast_values.append(ema_fast)
        ema_slow_values.append(ema_slow)

        macd = ema_fast - ema_slow # MACD is fast_MA - slow_EMA
        if ema_macd == 0:
            ema_macd = macd
        else:
            ema_macd = (macd - ema_macd) * K_macd + ema_macd # signal is EMA of MACD values

        macd_values.append(macd)
        macd_signal_values.append(ema_macd)
        macd_historgram_values.append(macd - ema_macd)

    goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
    goog_data = goog_data.assign(FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=goog_data.index))
    goog_data = goog_data.assign(SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=goog_data.index))
    goog_data = goog_data.assign(MovingAverageConvergenceDivergence=pd.Series(macd_values, index=goog_data.index))
    goog_data = goog_data.assign(Exponential20DayMovingAverageOfMACD=pd.Series(macd_signal_values, index=goog_data.index))
    goog_data = goog_data.assign(MACDHistorgram=pd.Series(macd_historgram_values, index=goog_data.index))

    close_price = goog_data['ClosePrice']
    ema_f = goog_data['FastExponential10DayMovingAverage']
    ema_s = goog_data['SlowExponential40DayMovingAverage']
    macd = goog_data['MovingAverageConvergenceDivergence']
    ema_macd = goog_data['Exponential20DayMovingAverageOfMACD']
    macd_histogram = goog_data['MACDHistorgram']
    goog_data['signal'] = pd.Series(np.zeros(len(goog_data)))
    goog_data['position'] = pd.Series(np.zeros(len(goog_data)))

    goog_data['signal'][0:] = np.where(macd[0:] > ema_macd[0:], 1.0, 0.0)
    goog_data['orders'] = goog_data['signal'].diff()

    print(goog_data)
    return goog_data

def macd_line_over_than_signal(pd_dataframe):
    df = macd(pd_dataframe)
    return df['MACDHistorgram'].iloc[-1] > 0


def macd_cross(pd_dataframe):
    df = macd(pd_dataframe)
    return df['orders'].iloc[-1] > 0
