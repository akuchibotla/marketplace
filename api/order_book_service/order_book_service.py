import jsonpickle
import configparser
from datetime import datetime
from bson.json_util import dumps
from .models.order import Order
from .utils.utils import binary_insert
from .models.order_book import OrderBook
from .db.mongodb_client import MongoDBClient
from .fifo_order_matcher import match_orders
from .utils.constants import BID_KEY, ASK_KEY

class OrderBookService:
    def __init__(self):
        self.__db_client__ = MongoDBClient(
            "mongodb+srv://akuchibotla:VwROlqUGJcNARaTLCifaFxHvlRAmBoXklzm@cluster0.clmvw.mongodb.net/marketplace?retryWrites=true&w=majority")

    def get_order_book(self, security, simplified=False):
        raw_order_book = self.__db_client__.get_orders(security)
        if raw_order_book:
            order_book = OrderBook(raw_order_book)
            if simplified:
                return {
                    'bids': order_book.get_bid_orders(),
                    'asks': order_book.get_ask_orders()
                }
            return order_book

    def get_securities(self):
        return self.__db_client__.get_securities()

    def place_order(self, security, side_key, price, volume, username, __socket__):
        # prepare new order and existing orders
        new_order = Order(price, volume, username)
        security_records = self.__db_client__.get_orders(security, True)
        spread_side_records = security_records[side_key]
        spread_side_orders = [Order(*order) for order in spread_side_records]

        # insert order according to the FIFO algorithm
        binary_insert(spread_side_orders, new_order, side_key)
        spread_side_order_tuples = [order.to_tuple() for order in spread_side_orders]

        # place order
        self.__db_client__.__update_record__(security, side_key, spread_side_order_tuples)

        # match orders
        order_book = self.get_order_book(security)
        matched_orders = match_orders(security, order_book, __socket__)
        if matched_orders:
            new_bids, new_asks = matched_orders['new_bids'], matched_orders['new_asks']
            self.__db_client__.__update_record__(security, BID_KEY, [bid.to_tuple() for bid in new_bids])
            self.__db_client__.__update_record__(security, ASK_KEY, [ask.to_tuple() for ask in new_asks])
        
        __socket__.emit('order_book_update', jsonpickle.encode(self.get_order_book(security, True)), namespace='/order-book')