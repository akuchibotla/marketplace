import unittest

from order_book_service.models.order import Order
from order_book_service.utils.constants import ASK_KEY, BID_KEY
from order_book_service.utils.utils import binary_insert

class TestInserts(unittest.TestCase):
    order1 = Order(price=50, volume=100, username='jayz')
    order2 = Order(price=51, volume=99, username='kanye')
    order3 = Order(price=51, volume=5, username='drake')
    order4 = Order(price=49, volume=4, username='lilwayne')

    def test_ask_inserts(self):
        """
        Test ask order inserts
        """
        orders = list()

        binary_insert(orders, self.order1, ASK_KEY)
        self.assertEqual(orders, [self.order1])

        binary_insert(orders, self.order2, ASK_KEY)
        self.assertEqual(orders, [self.order1, self.order2])

        binary_insert(orders, self.order3, ASK_KEY)
        self.assertEqual(orders, [self.order1, self.order2, self.order3])

        binary_insert(orders, self.order4, ASK_KEY)
        self.assertEqual(orders, [self.order4, self.order1, self.order2, self.order3])

    def test_bid_inserts(self):
        """
        Test bid order inserts
        """
        orders = list()

        binary_insert(orders, self.order1, BID_KEY)
        self.assertEqual(orders, [self.order1])

        binary_insert(orders, self.order2, BID_KEY)
        self.assertEqual(orders, [self.order2, self.order1])

        binary_insert(orders, self.order3, BID_KEY)
        self.assertEqual(orders, [self.order2, self.order3, self.order1])

        binary_insert(orders, self.order4, BID_KEY)
        self.assertEqual(orders, [self.order2, self.order3, self.order1, self.order4])

if __name__ == '__main__':
    unittest.main()