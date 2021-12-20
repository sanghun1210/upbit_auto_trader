
import time
from traders import *

class UpbitDataCenter():
    def __init__(self, coin_name):
        super().__init__()
        self.coin_name = coin_name
        self.market_group = None
        self.week_trader = None
        self.day_trader = None
        self.minute240_trader = None
        self.minute60_trader = None
        self.minute30_trader = None
        self.minute15_trader = None
        self.minute10_trader = None
        self.minute5_trader = None
        self.minute3_trader = None
        
        self.init_traders(coin_name)

    def init_traders(self, coin_name):
        # self.minute1_trader = Minute1Trader(coin_name, 120)
        # time.sleep(0.1)
        # self.minute3_trader = Minute3Trader(coin_name, 120)
        # time.sleep(0.15)
        # self.minute5_trader = Minute5Trader(coin_name, 120)
        # time.sleep(0.15)
        # self.minute10_trader = Minute10Trader(coin_name, 150)
        # time.sleep(0.1)
        # self.minute15_trader = Minute15Trader(coin_name, 120, src_logger)
        time.sleep(0.15)
        self.minute30_trader = Minute30Trader(coin_name, 160)
        time.sleep(0.15)
        self.minute60_trader = Minute60Trader(coin_name, 1000)
        time.sleep(0.15)
        self.minute240_trader = Minute240Trader(coin_name, 160)
        time.sleep(0.15)
        self.day_trader = DayTrader(coin_name, 120)
        time.sleep(0.15)
        self.week_trader = WeekTrader(coin_name, 60)