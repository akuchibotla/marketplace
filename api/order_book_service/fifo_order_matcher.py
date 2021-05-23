"""
Based loosely on https://en.wikipedia.org/wiki/Order_matching_system#Price/Time_algorithm_(or_First-in-First-out)
"""
import heapq
from datetime import datetime
from .utils.utils import get_mid_price
from .utils.constants import BID_KEY, ASK_KEY

def match_orders(security, order_book):
    all_bids, all_asks = \
        order_book.get_bid_orders(), order_book.get_ask_orders()

    update_required = False
    transactions = list()
    while all_bids and all_asks and all_bids[0].price >= all_asks[0].price:
        update_required = True
        curr_bid = all_bids.pop(0)
        curr_ask = all_asks.pop(0)
        midpoint_price = get_mid_price(curr_bid.price, curr_ask.price)

        smaller, larger = curr_bid, curr_ask
        smaller_all, larger_all = all_bids, all_asks
        smaller_key, larger_key = BID_KEY, ASK_KEY
        if curr_bid.volume > curr_ask.volume:
            smaller, larger = larger, smaller
            smaller_all, larger_all = larger_all, smaller_all
            smaller_key, larger_key = larger_key, smaller_key
        
        larger.volume -= smaller.volume
        if larger.volume > 0:
            larger_all.insert(0, larger)

        print('({}): {} sold {} shares of {} at ${}/share to {}'.format(\
            str(datetime.utcnow()), curr_ask.username, smaller.volume, security, midpoint_price, curr_bid.username))

        transactions.append({
            'price': midpoint_price,
            'volume': smaller.volume,
            'security': security,
            'payee': curr_bid.username,
            'payer': curr_ask.username,
            'timestamp': str(datetime.utcnow())
        })

    if update_required:
        return ({
            'new_bids': all_bids,
            'new_asks': all_asks,
            'transactions': transactions})