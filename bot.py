import json
from log import Log
from binance_f import RequestClient
from binance_f.model.constant import *


class Bot:
    def __init__(self):
        # read configuration from json file
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.api_url = config['api_url']
        self.sandbox = config['is_sandbox']
        self.percentage = float(config['percentage'])
        self.time = config['time']
        self.leverage = int(config['leverage'])
        self.size = int(config['size'])

        self.client = RequestClient(api_key=self.api_key, secret_key=self.api_secret, url=self.api_url)
        self.prices = {
            "before": {},
            "now": {}
        }

    def detect_mooning(self):
        if "before" not in self.prices or "now" not in self.prices:
            return

        for symbol, price in self.prices["now"].items():
            old_price = self.prices["before"][symbol]
            percentage = (price - old_price / old_price) * 100.0
            if abs(percentage) > self.percentage:
                print("mooning ! : " + symbol)
                self.add_order(
                    symbol=symbol,
                    price=price,
                    percentage=percentage
                )

    def get_all_prices(self):
        return self.client.get_symbol_price_ticker()

    def store_prices(self):
        self.prices["before"] = self.prices["now"]
        self.prices["now"] = {}

        prices = self.get_all_prices()
        for price in prices:
            self.prices["now"][price.symbol] = price.price

        return self.prices

    def add_order(self, symbol, price, percentage):
        if percentage > 0:
            side_order = OrderSide.BUY
            position_order = PositionSide.LONG
        else:
            side_order = OrderSide.SELL
            position_order = PositionSide.SHORT

        quantity = round(self.size / price, 5)

        Log.log_trade(
            symbol=symbol,
            position=position_order,
            quantity=quantity,
            price=price
        )

        if not self.sandbox:
            print("pouet")
            # self.client.post_order(
            #     symbol=symbol,
            #     side=side_order,
            #     positionSide=position_order,
            #     ordertype=OrderType.MARKET,
            #     quantity=quantity
            # )

    # def add_sl(self, symbol, price, ):