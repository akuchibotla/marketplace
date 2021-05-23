from datetime import datetime

class Order:
    def __init__(self, price, volume, username, timestamp=None):
        self.price = price
        self.volume = volume
        self.username = username
        self.timestamp = timestamp if timestamp else str(datetime.utcnow())
    
    def __lt__(self, other_order):
        return (self.price < other_order.price)\
            or (self.price == other_order.price\
                and self.timestamp < other_order.timestamp)

    def __gt__(self, other_order):
        return not self.price == other_order.price and not self.__lt__(other_order)
    
    def __eq__(self, other_order):
        return self.price == other_order.price\
            and self.volume == other_order.volume\
                and self.username == other_order.username\
                    and self.timestamp == other_order.timestamp

    def to_tuple(self):
        return (self.price, self.volume, self.username, self.timestamp)

    def copy(self):
        return Order(self.price, self.volume, self.username, self.timestamp)
