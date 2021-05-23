import bisect
from .constants import BID_KEY, ASK_KEY

def get_mid_price(min_ask_price, max_bid_price):
    return (max_bid_price + min_ask_price) / 2.0

def binary_insert(orders, new_order, side_key):
    if side_key == ASK_KEY:
        bisect.insort_right(orders, new_order)
    else:
        lo = 0
        hi = len(orders)
        while lo < hi:
            mid = (lo + hi) // 2
            if new_order > orders[mid]: hi = mid
            else: lo = mid+1
        orders.insert(lo, new_order)
