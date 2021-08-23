import os
import jwt
import uuid
import hashlib
import json
import time
from urllib.parse import urlencode

import requests

from .base_market import *
from .week_trader import *
from .day_trader import *
from .minute240_trader import *
from .minute60_trader import *
from .minute30_trader import *
from .minute15_trader import *
from .minute10_trader import *
        
access_key = 'y4YiH7yQ6IV7DH1kr8aaDxrNwrirvxqZxHRAY3gO'
secret_key = 'nKowNJTxJ1xyTiQLLNZp1G6NKYP5txsR2OxDY1DV'
server_url = 'https://api.upbit.com'
        
def get_my_markets():
    markets = []
    payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    time.sleep(0.1)

    json_markets = res.json()
    for json_market in json_markets:
        balance = MyMarket(json_market)
        markets.append(balance)

    return markets


class MyMarket(BaseMarket):
    def __init__(self, json):
        super().__init__()
        self.currency = json.get("currency")
        self.balance = json.get("balance")
        self.locked = json.get("locked")
        self.avg_buy_price = json.get("avg_buy_price")
        self.avg_buy_price_modified = json.get("avg_buy_price_modified")
        self.unit_currency = json.get("unit_currency")
        self.market_name = self.unit_currency + '-' + self.currency

    def is_go_down(self):
        minute60_trader = Minute60Trader(self.market_name, 20)
        return minute60_trader.is_go_down() 

    #매도
    def ask(self, market_name, money):            
        query = {
            'market': market_name,
            'side': 'bid',
            'volume': '',
            'price': str(money),
            'ord_type': 'market',
        }
        print(query)
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(self.server_url + "/v1/orders", params=query, headers=headers)


