"""
Interface for database client (can plug in any db solution)
"""
class DBClient():
    def __update_record__(self, security, side_key, spread_side_records):
        raise NotImplementedError('__update_record__ not implemented')

    def __initialize_security_records__(self, security):
        raise NotImplementedError('__initialize_security_records__ not implemented')
    
    def get_orders(self, security):
        raise NotImplementedError('get_orders not implemented')

    def get_securities(self):
        raise NotImplementedError('get_securities not implemented')