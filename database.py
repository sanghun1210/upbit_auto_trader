from market_log import MarketLog
import sqlite3
import requests


DB_name = 'myDB'

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
    conn = connect_to_db(DB_name)
    market_log = MarketLog(conn)
    #markets.create_table()

    market_log.insert_one('test', 'test')
    print(market_log.select_all())
    conn.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()


