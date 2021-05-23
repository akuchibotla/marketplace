import unittest
from datetime import datetime

from order_book_service.models.order import Order
from order_book_service.models.order_book import OrderBook
from order_book_service.fifo_order_matcher import match_orders
from order_book_service.utils.constants import ASK_KEY, BID_KEY

class TestMatcher(unittest.TestCase):
  def test_no_match(self):
    """
    Test simple order book match
    """
    ask_orders = [
      [500, 5, 'kanye', str(datetime.utcnow())],
      [505, 100, 'drake', str(datetime.utcnow())],
      [530, 105, 'jayz', str(datetime.utcnow())],
      [531, 4, 'lilwayne', str(datetime.utcnow())]
    ]

    bid_orders = [
      [499, 5, 'carti', str(datetime.utcnow())],
      [499, 15, 'travis', str(datetime.utcnow())],
      [498, 1000, 'uzi', str(datetime.utcnow())]
    ]

    order_book = OrderBook({ASK_KEY: ask_orders, BID_KEY: bid_orders})

    matched_orders = match_orders('TSLA', order_book)
    self.assertFalse(matched_orders)

  def test_equal_match(self):
    """
    Test simple order book match
    """
    ask_orders = [
      [500, 5, 'kanye', str(datetime.utcnow())], # should match
      [505, 100, 'drake', str(datetime.utcnow())],
      [530, 105, 'jayz', str(datetime.utcnow())],
      [531, 4, 'lilwayne', str(datetime.utcnow())]
    ]

    bid_orders = [
      [500, 5, 'carti', str(datetime.utcnow())], # should match
      [499, 15, 'travis', str(datetime.utcnow())],
      [498, 1000, 'uzi', str(datetime.utcnow())]
    ]

    order_book = OrderBook({ASK_KEY: ask_orders, BID_KEY: bid_orders})

    matched_orders = match_orders('TSLA', order_book)
    self.assertEqual(matched_orders['new_asks'],\
      [Order(*order_tuple) for order_tuple in ask_orders[1:]])
    self.assertEqual(matched_orders['new_bids'],\
      [Order(*order_tuple) for order_tuple in bid_orders[1:]])

  def test_remainder_ask(self):
    """
    More ask volume than bid volume for matched order
    """
    ask_orders = [
      [500, 25, 'kanye', str(datetime.utcnow())], # 20 units should remain
      [505, 100, 'drake', str(datetime.utcnow())],
      [530, 105, 'jayz', str(datetime.utcnow())],
      [531, 4, 'lilwayne', str(datetime.utcnow())]
    ]

    bid_orders = [
      [500, 5, 'carti', str(datetime.utcnow())], # should be completely matched
      [499, 15, 'travis', str(datetime.utcnow())],
      [498, 1000, 'uzi', str(datetime.utcnow())]
    ]

    order_book = OrderBook({ASK_KEY: ask_orders, BID_KEY: bid_orders})
    new_ask_orders = ask_orders[:]
    new_ask_orders[0][1] = 20

    matched_orders = match_orders('TSLA', order_book)
    self.assertEqual(matched_orders['new_asks'],\
      [Order(*order_tuple) for order_tuple in new_ask_orders])
    self.assertEqual(matched_orders['new_bids'],\
      [Order(*order_tuple) for order_tuple in bid_orders[1:]])

  def test_remainder_bid(self):
    """
    More bid volume than ask volume for matched order
    """
    ask_orders = [
      [500, 20, 'kanye', str(datetime.utcnow())], # should be completely matched
      [505, 100, 'drake', str(datetime.utcnow())],
      [530, 105, 'jayz', str(datetime.utcnow())],
      [531, 4, 'lilwayne', str(datetime.utcnow())]
    ]

    bid_orders = [
      [500, 50, 'carti', str(datetime.utcnow())], # 30 units should remain
      [499, 15, 'travis', str(datetime.utcnow())],
      [498, 1000, 'uzi', str(datetime.utcnow())]
    ]

    order_book = OrderBook({ASK_KEY: ask_orders, BID_KEY: bid_orders})
    new_bid_orders = bid_orders[:]
    new_bid_orders[0][1] = 30

    matched_orders = match_orders('TSLA', order_book)
    self.assertEqual(matched_orders['new_asks'],\
      [Order(*order_tuple) for order_tuple in ask_orders[1:]])
    self.assertEqual(matched_orders['new_bids'],\
      [Order(*order_tuple) for order_tuple in new_bid_orders])

  def test_cleared_ask(self):
    """
    One ask clearing all remaining bids
    """
    ask_orders = [
      [470, 30, 'kanye', str(datetime.utcnow())], # matches all bids
    ]

    bid_orders = [
      [500, 5, 'carti', str(datetime.utcnow())],
      [499, 15, 'travis', str(datetime.utcnow())],
      [498, 10, 'uzi', str(datetime.utcnow())]
    ]

    order_book = OrderBook({ASK_KEY: ask_orders, BID_KEY: bid_orders})

    matched_orders = match_orders('TSLA', order_book)
    self.assertEqual(matched_orders['new_asks'], [])
    self.assertEqual(matched_orders['new_bids'], [])

  def test_cleared_bid(self):
    """
    One bid clearing all remaining asks
    """
    ask_orders = [
      [500, 20, 'kanye', str(datetime.utcnow())],
      [505, 30, 'drake', str(datetime.utcnow())],
      [530, 40, 'jayz', str(datetime.utcnow())],
      [531, 50, 'lilwayne', str(datetime.utcnow())]
    ]

    bid_orders = [
      [600, 140, 'carti', str(datetime.utcnow())], # matches all asks
    ]

    order_book = OrderBook({ASK_KEY: ask_orders, BID_KEY: bid_orders})

    matched_orders = match_orders('TSLA', order_book)
    self.assertEqual(matched_orders['new_asks'], [])
    self.assertEqual(matched_orders['new_bids'], [])

if __name__ == '__main__':
    unittest.main()