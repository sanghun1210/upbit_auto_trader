import sqlite3
import datetime
from sqlite3 import OperationalError, IntegrityError, ProgrammingError

class MarketLog():
    def __init__(self, connect):
        self.conn = connect
        self.table_name = 'market_log'

    def tuple_to_dict(self, src_tuple):
        mydict = dict()
        mydict['date_time'] = src_tuple[0]
        mydict['market_name'] = src_tuple[1]
        mydict['price'] = src_tuple[2]
        return mydict

    def create_table(self):
        sql = 'CREATE TABLE {} (date_time TEXT,' \
          'market_name TEXT, price TEXT)'.format(self.table_name)

        try:
            self.conn.execute(sql)
        except OperationalError as e:
            print(e)
        
    def insert_one(self, market_name, price):
        sql = "INSERT INTO {} ('date_time', 'market_name', 'price') VALUES (?, ?, ?)"\
            .format(self.table_name)
        try:
            now = datetime.datetime.now()
            nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            self.conn.execute(sql, (nowDatetime, market_name, price))
            self.conn.commit()
        except Exception as e:
            print(e)

    def select_all(self):
        sql = 'SELECT * FROM {}'.format(self.table_name)
        c = self.conn.execute(sql)
        results = c.fetchall()
        return list(map(lambda x: self.tuple_to_dict(x), results))



