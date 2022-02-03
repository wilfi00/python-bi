class Log:

    @staticmethod
    def log_trade(symbol, position, quantity, price):
        print("New trade for symbol " + symbol + " en " + position + " de " + str(quantity) + " à " + str(price))
