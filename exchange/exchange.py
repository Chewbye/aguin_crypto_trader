import ccxt
import time

class Exchange(object):
    def __init__(self, exchange_id: str, api_key: str=None, secret: str=None):
        self.exchange_id = exchange_id
    
    def _init_exchange(self, api_key: str, secret: str):
        self._exchange_class = getattr(ccxt, self.exchange_id)
        self.exchange = self._exchange_class({
            'apiKey': api_key,
            'secret': secret
        })

    def __new__(cls, exchange_id: str, api_key: str=None, secret: str=None, _cache={}):
        try:
            return _cache[exchange_id]
        except KeyError:
            # you must call __new__ on the base class
            x = super(Exchange, cls).__new__(cls)
            x.__init__(exchange_id)
            x._init_exchange(api_key, secret)
            _cache[exchange_id] = x
            return x

    def get_historical_data(self, symbol, timeframe = '1d', since = None, limit = None, params = {} ):
        if self.exchange.has['fetchOHLCV']:
            data = self.exchange.fetchOHLCV(symbol, timeframe = timeframe, since = since, limit = limit, params = params)
            return ''.join(str(x) for x in data)
