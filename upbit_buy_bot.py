import requests
import json
import time
from mail import *
import datetime
import sqlite3

from markets.upbit_market import *
from markets.market_log import *
from sqlite3 import OperationalError, IntegrityError, ProgrammingError

import logging

DB_name = 'KRW_DB'

def connect_to_db(db=None):
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection

def main():
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('upbit_info.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logdb_connection = connect_to_db(DB_name)
        market_log = MarketLog(logdb_connection)
        market_log.create_table()

        upbit_market = UpbitMarket(logdb_connection, logger)
        best_market_names = upbit_market.find_best_markets('KRW')
    except Exception as e:    
        print("raise error ", e)
if __name__ == "__main__":
    # execute only if run as a script
    main()
