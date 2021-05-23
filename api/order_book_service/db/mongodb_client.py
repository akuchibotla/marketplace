import heapq
import jsonpickle
from datetime import datetime
from .db_client import DBClient
from pymongo import MongoClient
from ..models.order import Order
from ..utils.constants import BID_KEY, ASK_KEY

class MongoDBClient(DBClient):
    def __init__(self, conn_str=None):
        if conn_str:
            assert type(conn_str) == str
            self.__client__ = MongoClient(conn_str)
        else:
            self.__client__ = MongoClient()
        
        self.__conn_str__ = conn_str
        self.__collection__ = self.__client__.marketplace
        self.__order_book__ = self.__collection__.order_book

    def __update_record__(self, security, side_key, spread_side_records):
        filter_query = {'security': security}
        update = {'$set': {side_key: spread_side_records}}
        self.__order_book__.update_one(filter_query, update)

    def __initialize_security_records__(self, security):
        self.__order_book__.insert_one({'security': security, ASK_KEY: list(), BID_KEY: list()})
    
    def get_orders(self, security, write_if_empty=False):
        security_records = self.__order_book__.find_one({'security': security})
        if not security_records and write_if_empty:
            self.__initialize_security_records__(security)
            return self.get_orders(security)
        return security_records

    def get_securities(self):
        return self.__order_book__.distinct('security')