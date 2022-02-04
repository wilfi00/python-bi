import json
import time
from log import Log
from binance_f import RequestClient
from binance_f.model.constant import *
import utils


class Bot:
    def __init__(self):
        # read configuration from json file
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.api_url = config['api_url']
        self.sandbox = config['is_sandbox'] == "True"
        self.percentage = float(config['percentage'])
        self.sl_percentage = float(config['sl_percentage'])
        self.tp_percentage = float(config['tp_percentage'])
        self.time = int(config['time'])
        self.leverage = int(config['leverage'])
        self.size = int(config['size'])

        self.client = RequestClient(api_key=self.api_key, secret_key=self.api_secret, url=self.api_url)
        self.prices = {
            "before": {},
            "now": {}
        }

    def run(self):
        while 1:
            self.store_prices()
            time.sleep(self.time)
            self.store_prices()
            self.detect_mooning()

    def detect_mooning(self):
        if "before" not in self.prices or "now" not in self.prices:
            return

        for symbol, price in self.prices["now"].items():
            old_price = self.prices["before"][symbol]
            percentage = ((price - old_price) / old_price) * 100.0
            if abs(percentage) > self.percentage:
                print("mooning ! : " + symbol + " " + str(percentage))
                print("current price : " + str(price))
                print("old price : " + str(old_price))
                quantity = utils.truncate((self.size / price), 4)
                self.add_order(
                    symbol=symbol,
                    price=price,
                    percentage=percentage,
                    quantity=quantity
                )
                self.add_sl(
                    symbol=symbol,
                    price=price,
                    old_price=old_price,
                    percentage=percentage,
                    quantity=quantity
                )
                self.add_tp(
                    symbol=symbol,
                    price=price,
                    old_price=old_price,
                    percentage=percentage,
                    quantity=quantity
                )

    def get_all_prices(self):
        return self.client.get_symbol_price_ticker()

    def store_prices(self):
        self.prices["before"] = self.prices["now"]
        self.prices["now"] = {}

        prices = self.get_all_prices()
        for price in prices:
            if price.symbol[-4:] == "USDT":
                self.prices["now"][price.symbol] = price.price

        return self.prices

    def add_order(self, symbol, price, percentage, quantity):
        if utils.is_buying(percentage):
            side_order = OrderSide.BUY
            position_order = PositionSide.LONG
        else:
            side_order = OrderSide.SELL
            position_order = PositionSide.SHORT

        Log.log_trade(
            symbol=symbol,
            position=position_order,
            quantity=quantity,
            price=price
        )

        if not self.sandbox:
            self.client.change_initial_leverage(
                symbol=symbol,
                leverage=self.leverage
            )
            # self.client.change_margin_type(
            #     symbol=symbol,
            #     marginType=FuturesMarginType.ISOLATED
            # )
            return self.client.post_order(
                symbol=symbol,
                side=side_order,
                # positionSide=position_order,
                ordertype=OrderType.MARKET,
                quantity=quantity
            )

    def add_sl(self, symbol, price, old_price, percentage, quantity):
        sl_price = abs(float((price - old_price) * self.sl_percentage))

        if utils.is_buying(percentage):
            sl_price = utils.truncate(price - sl_price, 4)
            side_order = OrderSide.SELL
        else:
            sl_price = utils.truncate(price + sl_price, 4)
            side_order = OrderSide.BUY

        Log.log_sl(
            symbol=symbol,
            quantity=quantity,
            price=sl_price
        )

        if not self.sandbox:
            return self.client.post_order(
                symbol=symbol,
                side=side_order,
                ordertype=OrderType.STOP_MARKET,
                stopPrice=sl_price,
                closePosition=True,
                workingType=WorkingType.MARK_PRICE
            )

    def add_tp(self, symbol, price, old_price, percentage, quantity):
        tp_price = abs(float((price - old_price) * self.tp_percentage))
        if utils.is_buying(percentage):
            tp_price = utils.truncate(price + tp_price, 4)
            side_order = OrderSide.SELL
        else:
            tp_price = utils.truncate(price - tp_price, 4)
            side_order = OrderSide.BUY

        Log.log_tp(
            symbol=symbol,
            quantity=quantity,
            price=tp_price
        )

        if not self.sandbox:
            return self.client.post_order(
                symbol=symbol,
                side=side_order,
                ordertype=OrderType.TAKE_PROFIT_MARKET,
                stopPrice=tp_price,
                closePosition=True,
                workingType=WorkingType.MARK_PRICE
            )
