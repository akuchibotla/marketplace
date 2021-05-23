from ..utils.constants import BID_KEY, ASK_KEY
from .order import Order

class OrderBook:
    def __init__(self, order_book):
        self.__order_book__ = order_book

        raw_bid_orders = order_book[BID_KEY]
        raw_ask_orders = order_book[ASK_KEY]
    
        bid_orders, ask_orders = list(map(self.__convert_order_tuples_to_orders__, \
            [raw_bid_orders, raw_ask_orders]))

        order_book[BID_KEY] = bid_orders
        order_book[ASK_KEY] = ask_orders

    def __convert_order_tuples_to_orders__(self, order_tuples):
        return list(map(lambda order_tuple: Order(*order_tuple), order_tuples))

    def get_bid_orders(self):
        return self.__order_book__[BID_KEY]

    def get_max_bid_order(self):
        bid_orders = self.get_bid_orders()
        if bid_orders:
            return self.get_bid_orders()[0]

    def get_ask_orders(self):
        return self.__order_book__[ASK_KEY]
    
    def get_min_ask_order(self):
        ask_orders = self.get_ask_orders()
        if ask_orders:
            return self.get_ask_orders()[0]