import os
import jwt
import uuid
import hashlib
import json
import time
from urllib.parse import urlencode

import requests

class Balance():
    def __init__(self, json_data):
        self.currency = 'KRW-' + json_data.get("currency")
        self.balance = json_data.get("balance")
        self.avg_buy_price = json_data.get("avg_buy_price")
        self.unit_currency = json_data.get("unit_currency") 

class Store():
    def __init__(self):
        self.access_key = 'y4YiH7yQ6IV7DH1kr8aaDxrNwrirvxqZxHRAY3gO'
        self.secret_key = 'nKowNJTxJ1xyTiQLLNZp1G6NKYP5txsR2OxDY1DV'
        self.server_url = 'https://api.upbit.com'

    def get_balance_list(self):

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + "/v1/accounts", headers=headers)
        balances = []

        length = len(res.json())
        for i in range(0, int(length)):
            balance = Balance(res.json()[i])
            balances.append(balance)
        return balances

    def is_already_have(self, market_name):
        query = {
            'market': market_name,
        }
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

        res = requests.get(self.server_url + "/v1/orders/chance", params=query, headers=headers)
        #print(res.json())

        ask_account = res.json()["ask_account"]
        coin_balance = ask_account["balance"]
        
        is_already_have_this = (coin_balance != '0.0')
        #print("is_already_have_this coin : ", is_already_have_this, market_name)
        return is_already_have_this

        
    def buy(self, market_name, volume, price):            
        query = {
            'market': market_name,
            'side': 'bid',
            'volume': str(volume),  #balance
            'price': str(price),
            'ord_type': 'limit',
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

    def sell(self, market_name, volume, price):            
        query = {
            'market': market_name,
            'side': 'ask',
            'volume': str(volume),  #balance
            'price': str(price),
            'ord_type': 'limit',
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





    