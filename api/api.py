import json
import jsonpickle
from flask_socketio import SocketIO, emit, disconnect
from flask import Flask, request, Response, make_response, session
from order_book_service.order_book_service import OrderBookService
from order_book_service.utils.constants import BID_KEY, ASK_KEY, SELL_ORDER, BUY_ORDER

app = Flask(__name__)
__socket__ = SocketIO(app, async_mode=None)
order_book_service = OrderBookService()

@app.route('/order-book/<security>', methods=['GET'])
def get_orders(security):
    order_book = order_book_service.get_order_book(security, True)
    return jsonpickle.encode(order_book, unpicklable=False)

@app.route('/securities', methods=['GET'])
def get_securities():
    securities = order_book_service.get_securities()
    return jsonpickle.encode(securities, unpicklable=False)

@app.route('/order/<security>', methods=['POST'])
def post_order(security):
    content = request.json

    for required_key in ['order_type', 'price', 'volume', 'username']:
        assert(required_key in content)

    order_type = content['order_type'].upper()
    price = float(content['price'])
    volume = int(content['volume'])
    username = content['username']

    assert(price > 0)
    assert(volume > 0)
    assert(order_type in [SELL_ORDER, BUY_ORDER])

    side_key = ASK_KEY if order_type == SELL_ORDER else BID_KEY

    order_book_service.place_order(security, side_key, price, volume, username, __socket__)
    return make_response('OK', 200)

@__socket__.on('connection_event', namespace='/order-book')
def ws_connection(message):
    print('connected!')
    __socket__.emit('order_book_update', get_orders(message['data']), namespace='/order-book')

if __name__ == '__main__':
    __socket__.run(app, debug=True)