import pandas as pd

from pandas_datareader import data

'''

The Simple Moving Average (SMA) is calculated
 by adding the price of an instrument over a number of time periods
 and then dividing the sum by the number of time periods. The SMA
 is basically the average price of the given time period, with equal
 weighting given to the price of each period.

Simple Moving Average
SMA = ( Sum ( Price, n ) ) / n    

Where: n = Time Period
'''
import statistics as stats

#단순 이동 평균
def sma(pd_dataframe):
    close = pd_dataframe['trade_price']
    time_period = 20 # number of days over which to average
    history = [] # to track a history of prices
    sma_values = [] # to track simple moving average values
    for close_price in close:
        history.append(close_price)
        if len(history) > time_period: # we remove oldest price because we only average over last 'time_period' prices
            del (history[0])

        sma_values.append(stats.mean(history))

    pd_dataframe = pd_dataframe.assign(ClosePrice=pd.Series(close, index=pd_dataframe.index))
    pd_dataframe = pd_dataframe.assign(Simple20DayMovingAverage=pd.Series(sma_values, index=pd_dataframe.index))

    close_price = pd_dataframe['ClosePrice']
    sma = pd_dataframe['Simple20DayMovingAverage']

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Google price in $')
    close_price.plot(ax=ax1, color='g', lw=2., legend=True)
    sma.plot(ax=ax1, color='r', lw=2., legend=True)
    plt.show()
