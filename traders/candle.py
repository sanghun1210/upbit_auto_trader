class Candle():
    def __init__(self, index, json_candle):
        self.market = json_candle.get("market")
        self.candle_date_time_utc = json_candle.get("candle_date_time_utc")
        self.candle_date_time_kst = json_candle.get("candle_date_time_kst")
        self.opening_price = json_candle.get("opening_price") #시가
        self.high_price = json_candle.get("high_price")
        self.trade_price = json_candle.get("trade_price") #종가
        self.candle_acc_trade_price = json_candle.get("candle_acc_trade_price")
        self.candle_acc_trade_volume = json_candle.get("candle_acc_trade_volume")
        self.low_price = json_candle.get("low_price")
        self.index = index

    def is_yangbong(self):
        return (self.trade_price - self.opening_price) > 0

    def get_yangbong_rate(self):
        rate = ((self.trade_price - self.opening_price) / self.trade_price) * 100
        return rate

    def get_umbong_rate(self):
        rate = ((self.opening_price - self.trade_price ) / self.opening_price) * 100
        return rate

        
