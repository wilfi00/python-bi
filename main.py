import bot
from pprint import pprint
import time
import utils

if __name__ == '__main__':
    bot = bot.Bot()
    bot.run()

    # symbol = "ATAUSDT"
    # old_price = 0.4136
    # price = 0.4117
    # percentage = -1
    # quantity = float(utils.truncate((10 / price), 0))
    #
    # result_order = bot.add_order(
    #     symbol="ATAUSDT",
    #     price=price,
    #     percentage=percentage,
    #     quantity=quantity
    # )
    # result_sl = bot.add_sl(
    #     symbol=symbol,
    #     price=price,
    #     old_price=old_price,
    #     percentage=percentage,
    #     quantity=quantity
    # )
    # result_tp = bot.add_tp(
    #     symbol=symbol,
    #     price=price,
    #     old_price=old_price,
    #     percentage=percentage,
    #     quantity=quantity
    # )
    # print(result_order)
    # print(result_sl)
    # print(result_tp)
