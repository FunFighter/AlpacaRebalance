#! /usr/bin/env python3
import alpaca_trade_api as alpaca
from tools import *
from keys import *
import time

api = alpaca.REST(apiKey,secretKey, 'https://paper-api.alpaca.markets')

# only run if the market is open duh
if (api.get_clock().is_open):
    stdSeriese = GetSTD('TQQQ','minute',rollingSize=390)
    std = stdSeriese[-1]
    if (std<1.2):
        print(f'{std}')
        if (GetStockQty('SQQQ') < 1):
            # GTFO()
            time.sleep(10)
            BuyPercentage('TQQQ', 1.0)

        elif (GetStockQty('SQQQ') > 1):
            GTFO()
            BuyPercentage('TQQQ', 1.0)

    else:
        print(f'{std}')
        if (GetStockQty('TQQQ') < 1):
            # GTFO()
            time.sleep(10)
            BuyPercentage('SQQQ', 1.0)

        elif (GetStockQty('TQQQ') > 1):
            GTFO()
            BuyPercentage('SQQQ', 1.0)

else:
    print('The market is {}'.format('open.' if api.get_clock().is_open else 'closed.'))


