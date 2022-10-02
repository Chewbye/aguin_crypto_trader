from exchange.exchange import Exchange
from scripts.config import Config
import os
import time


def download_data(args):

    conf = Config(args['conf'])
    exchange_name = conf.get("exchange")["name"]
    exchange = Exchange(exchange_name)

    symbols = conf.get("pairs")
    for symbol in symbols:
        print("Downloading data " + symbol)
        data = exchange.get_historical_data(symbol, limit = args["days"])
        if data == None:
            print("No data for symbol " + symbol)
        else:
            filename = "data/" + exchange_name + "/" + symbol.replace("/", "") + "_" + conf.get("timeframe") + ".csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(data)
            time.sleep (exchange.exchange.rateLimit / 1000) # time.sleep wants seconds


