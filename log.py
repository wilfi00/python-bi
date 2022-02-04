class Log:

    @staticmethod
    def log_trade(symbol, position, quantity, price):
        print("New trade symbole " + symbol + " en " + position + " de quantité " + str(quantity) + " au prix " + str(
            price))

    @staticmethod
    def log_sl(symbol, quantity, price):
        print("Ajout du SL pour le symbole " + symbol + " de quantité " + str(quantity) + " au prix " + str(price))

    @staticmethod
    def log_tp(symbol, quantity, price):
        print("Ajout du TP pour le symbole " + symbol + " de quantité " + str(quantity) + " au prix " + str(price))
