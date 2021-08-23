import requests
import json
import time
from mail import *
import datetime
import sqlite3

from markets.upbit_market import *
from markets.market_log import *
from sqlite3 import OperationalError, IntegrityError, ProgrammingError

DB_name = 'BTC_DB'

def connect_to_db(db=None):
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection

def get_anaylize_str(stats):
    strlist = []
    stat_count = 0 
    for stat in stats:
        strlist.append(stat[0] + ' : ' + str(stat[1]))
        stat_count = stat_count + 1
        if stat_count > 12:
            break;
    return '\r\n'.join(strlist)

    
def main():
    try:
        loop_count = 1
        logdb_connection = connect_to_db(DB_name)
        market_log = MarketLog(logdb_connection)
        market_log.create_table()
        # to_send_mail_str_log = get_anaylize_str(market_log.analyze())
        # print(to_send_mail_str_log)
        while True:
            upbit_market = UpbitMarket(logdb_connection)
            best_market_names = upbit_market.find_best_markets('BTC')
        
            if int(len(best_market_names)) > 0:
                current_result = '\r\n'.join(best_market_names)
                to_send_mail_str_log = get_anaylize_str(market_log.analyze())
                send_mail(current_result + '\r\n'+ '\r\n' + to_send_mail_str_log, "check result")
            loop_count = loop_count + 1  
            time.sleep(150)
    except Exception as e:    
        print("raise error ", e)
if __name__ == "__main__":
    # execute only if run as a script
    main()
