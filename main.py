from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

class Bot():
    def __init__(self):
        # read configuration from json file
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.api_passphrase = config['api_passphrase']
        self.sandbox = config['is_sandbox']
        self.symbol_a = config['symbol_a']
        self.symbol_b = config['symbol_b']
        self.spread_mean = float(config['spread_mean'])
        self.leverage = float(config['leverage'])
        self.size = int(config['size'])
        self.num_param = float(config['num_param'])
        self.trade = Trade(self.api_key, self.api_secret, self.api_passphrase, is_sandbox=self.sandbox)
        self.market = Market(self.api_key, self.api_secret, self.api_passphrase, is_sandbox=self.sandbox)


if __name__ == '__main__':
    hf = Bot()











client = Client('', '')

# get market depth
depth = client.get_order_book(symbol='BNBBTC')
print('depth')
print(depth)

# place a test market buy order, to place an actual order use the create_order function
order = client.create_test_order(
    symbol='BNBBTC',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=100)
print('order')
print(order)

# get all symbol prices
prices = client.get_all_tickers()
print('prices')
print(prices)

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
print('klines')
print(klines)
