
import time
from traders import *

class UpbitDataCenter():
    def __init__(self, market_name):
        super().__init__()
        self.market_name = market_name
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
        
        self.init_traders(market_name)

    def init_traders(self, market_name):
        # self.minute1_trader = Minute1Trader(market_name, 120)
        # time.sleep(0.1)
        # self.minute3_trader = Minute3Trader(market_name, 120)
        # time.sleep(0.1)
        # self.minute5_trader = Minute5Trader(market_name, 120, src_logger)
        # time.sleep(0.1)
        self.minute10_trader = Minute10Trader(market_name, 200)
        time.sleep(0.1)
        # self.minute15_trader = Minute15Trader(market_name, 120, src_logger)
        # time.sleep(0.1)
        self.minute30_trader = Minute30Trader(market_name, 150)
        time.sleep(0.15)
        # self.minute60_trader = Minute60Trader(market_name, 400)
        # time.sleep(0.15)
        # self.minute240_trader = Minute240Trader(market_name, 80)
        # time.sleep(0.15)
        # self.day_trader = DayTrader(market_name, 100)
        # time.sleep(0.15)
        # self.week_trader = WeekTrader(market_name, 20, src_logger)