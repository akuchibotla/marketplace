"""
Interface for database client (can plug in any db solution)

Data Model
==========
{
    ticker: {
        bid: [(bid_price, volume, username), (bid_price, volume, username)...],
        ask: [(ask_price, volume, username), (ask_price, volume, username)...]
    }
    TSLA: {
        # max heap (using negative dollar amounts + min heap)
        bid: [(-600.05, 3, harry), (-600.01, 42, anand), (-598.98, 50, zain), ...],
        # min heap
        ask: [(601.77, 40, elon), (601.81, 3, chamath), ...]  # min heap
}}
"""
class DBClient():
    def __init__(self, conn_str=None):
        raise NotImplementedError('constructor not implemented')
    
    def get_orders(self, security):
        raise NotImplementedError('get_orders not implemented')

    def place_order(self, security, side_key, price, volume, username):
        raise NotImplementedError('place_order not implemented')