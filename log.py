class Log:

    @staticmethod
    def log_trade(symbol, position, quantity, price):
        print("New trade symbole " + symbol + " en " + position + " de quantité " + str(quantity) + " au prix " + str(price))
