import pandas as pd

from pandas_datareader import data
import numpy as np

def bbands(pd_dataframe): 
    goog_data = pd_dataframe
    close = goog_data['trade_price']

    import statistics as stats
    import math as math

    time_period = 14 # history length for Simple Moving Average for middle band
    stdev_factor = 2 # Standard Deviation Scaling factor for the upper and lower bands
    history = [] # price history for computing simple moving average
    sma_values = [] # moving average of prices for visualization purposes
    upper_band = [] # upper band values
    lower_band = [] # lower band values

    for close_price in close:
        history.append(close_price)
        if len(history) > time_period: # we only want to maintain at most 'time_period' number of price observations
            del (history[0])

        sma = stats.mean(history)
        sma_values.append(sma) # simple moving average or middle band
        variance = 0 # variance is the square of standard deviation
        for hist_price in history:
            variance = variance + ((hist_price - sma) ** 2)

        stdev = math.sqrt(variance / len(history)) # use square root to get standard deviation

        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)

    goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
    goog_data = goog_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=goog_data.index))
    goog_data = goog_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(upper_band, index=goog_data.index))
    goog_data = goog_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(lower_band, index=goog_data.index))

    close_price = goog_data['ClosePrice']
    mband = goog_data['MiddleBollingerBand20DaySMA']
    uband = goog_data['UpperBollingerBand20DaySMA2StdevFactor']
    lband = goog_data['LowerBollingerBand20DaySMA2StdevFactor']

    goog_data['buy_signal'] =\
        np.where(goog_data['LowerBollingerBand20DaySMA2StdevFactor'][0:]
                                                > goog_data['trade_price'][0:], 1.0, 0.0)

    goog_data['buy_orders'] = goog_data['buy_signal'].diff()

    goog_data['sell_signal'] =\
        np.where(goog_data['MiddleBollingerBand20DaySMA'][0:]
                                                < goog_data['trade_price'][0:], -1.0, 0.0)
    goog_data['sell_orders'] = goog_data['sell_signal'].diff()

    # initial_capital = float(1000.0)
    # positions = pd.DataFrame(index=goog_data.index).fillna(0.0)
    # portfolio = pd.DataFrame(index=goog_data.index).fillna(0.0)
    # positions['GOOG'] = goog_data['signal'] 

    # portfolio['positions'] = (positions.multiply(goog_data['trade_price'], axis = 0))

    # portfolio['cash'] = initial_capital - (positions.diff().multiply(goog_data['trade_price'], axis=0)).cumsum()
    # portfolio['total'] = portfolio['positions'] + portfolio['cash']

    # print(portfolio)


    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Google price in $')

    ax1.plot(goog_data.loc[goog_data.buy_orders== 1.0].index,
            pd_dataframe["trade_price"][goog_data.buy_orders == 1.0],
            '^', markersize=7, color='k')

    ax1.plot(goog_data.loc[goog_data.sell_orders== -1.0].index,
            pd_dataframe["trade_price"][goog_data.sell_orders == -1.0],
            'v', markersize=7, color='k')

    close_price.plot(ax=ax1, color='g', lw=2., legend=True)
    mband.plot(ax=ax1, color='b', lw=2., legend=True)
    uband.plot(ax=ax1, color='g', lw=2., legend=True)
    lband.plot(ax=ax1, color='r', lw=2., legend=True)
    plt.show()


def bbands_is_low_touch(pd_dataframe):
    goog_data = pd_dataframe
    close = goog_data['trade_price']

    import statistics as stats
    import math as math

    time_period = 14 # history length for Simple Moving Average for middle band
    stdev_factor = 2 # Standard Deviation Scaling factor for the upper and lower bands
    history = [] # price history for computing simple moving average
    sma_values = [] # moving average of prices for visualization purposes
    upper_band = [] # upper band values
    lower_band = [] # lower band values

    for close_price in close:
        history.append(close_price)
        if len(history) > time_period: # we only want to maintain at most 'time_period' number of price observations
            del (history[0])

        sma = stats.mean(history)
        sma_values.append(sma) # simple moving average or middle band
        variance = 0 # variance is the square of standard deviation
        for hist_price in history:
            variance = variance + ((hist_price - sma) ** 2)

        stdev = math.sqrt(variance / len(history)) # use square root to get standard deviation

        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)

    goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
    goog_data = goog_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=goog_data.index))
    goog_data = goog_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(upper_band, index=goog_data.index))
    goog_data = goog_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(lower_band, index=goog_data.index))

    close_price = goog_data['ClosePrice']
    mband = goog_data['MiddleBollingerBand20DaySMA']
    uband = goog_data['UpperBollingerBand20DaySMA2StdevFactor']
    lband = goog_data['LowerBollingerBand20DaySMA2StdevFactor']

    goog_data['buy_signal'] =\
        np.where(goog_data['LowerBollingerBand20DaySMA2StdevFactor'][0:]
                                                > goog_data['trade_price'][0:], 1.0, 0.0)

    goog_data['buy_orders'] = goog_data['buy_signal'].diff()

    goog_data['sell_signal'] =\
        np.where(goog_data['MiddleBollingerBand20DaySMA'][0:]
                                                < goog_data['trade_price'][0:], -1.0, 0.0)
    goog_data['sell_orders'] = goog_data['sell_signal'].diff()
    return goog_data['buy_orders'].iloc[-1] > 0

def bbands_is_middle_touch(pd_dataframe):
    goog_data = pd_dataframe
    close = goog_data['trade_price']

    import statistics as stats
    import math as math

    time_period = 14 # history length for Simple Moving Average for middle band
    stdev_factor = 2 # Standard Deviation Scaling factor for the upper and lower bands
    history = [] # price history for computing simple moving average
    sma_values = [] # moving average of prices for visualization purposes
    upper_band = [] # upper band values
    lower_band = [] # lower band values

    for close_price in close:
        history.append(close_price)
        if len(history) > time_period: # we only want to maintain at most 'time_period' number of price observations
            del (history[0])

        sma = stats.mean(history)
        sma_values.append(sma) # simple moving average or middle band
        variance = 0 # variance is the square of standard deviation
        for hist_price in history:
            variance = variance + ((hist_price - sma) ** 2)

        stdev = math.sqrt(variance / len(history)) # use square root to get standard deviation

        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)

    goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
    goog_data = goog_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=goog_data.index))
    goog_data = goog_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(upper_band, index=goog_data.index))
    goog_data = goog_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(lower_band, index=goog_data.index))

    close_price = goog_data['ClosePrice']
    mband = goog_data['MiddleBollingerBand20DaySMA']
    uband = goog_data['UpperBollingerBand20DaySMA2StdevFactor']
    lband = goog_data['LowerBollingerBand20DaySMA2StdevFactor']

    goog_data['buy_signal'] =\
        np.where(goog_data['LowerBollingerBand20DaySMA2StdevFactor'][0:]
                                                > goog_data['trade_price'][0:], 1.0, 0.0)

    goog_data['buy_orders'] = goog_data['buy_signal'].diff()

    goog_data['sell_signal'] =\
        np.where(goog_data['MiddleBollingerBand20DaySMA'][0:]
                                                < goog_data['trade_price'][0:], -1.0, 0.0)
    goog_data['sell_orders'] = goog_data['sell_signal'].diff()
    return goog_data['sell_orders'].iloc[-1] < 0