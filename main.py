import bot
from pprint import pprint
import time


if __name__ == '__main__':
    bot = bot.Bot()

    # while 1:
    bot.store_prices()
    time.sleep(60)
    bot.store_prices()
    bot.detect_mooning()
    # bot.detect_mooning()



