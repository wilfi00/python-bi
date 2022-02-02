from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
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
