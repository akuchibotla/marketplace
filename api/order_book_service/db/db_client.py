"""
Interface for database client (can plug in any db solution)
"""
class DBClient():
    def __init__(self, conn_str=None):
        raise NotImplementedError('constructor not implemented')

    def __update_record__(self, security, side_key, spread_side_records):
        raise NotImplementedError('__update_record__ not implemented')
    
    def get_orders(self, security):
        raise NotImplementedError('get_orders not implemented')

    def get_securities(self):
        raise NotImplementedError('get_securities not implemented')