import requests
import json
import time
from mail import *
import datetime

from markets.my_market import *
    
def main():
    try:
        while True:
            my_markets = get_my_markets()
            down_markets = []
            for market in my_markets:
                if market.market_name == "KRW-KRW":
                    continue

                if market.is_go_down():
                    down_markets.append(market.market_name)
                    print('haha - go to sell', market.market_name)
                    

            if int(len(down_markets)) > 0:
                send_mail('\r\n'.join(down_markets), "go to sell")
            time.sleep(250)
    except Exception as e:    
        print("raise error ", e)
if __name__ == "__main__":
    # execute only if run as a script
    main()
