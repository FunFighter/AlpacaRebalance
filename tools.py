import alpaca_trade_api as alpaca
from keys import *

api = alpaca.REST(apiKey,secretKey, 'https://paper-api.alpaca.markets')

def GetSTD(ticker = 'TQQQ',timeSet = 'minute',rollingSize = 390):
    stock = api.get_barset(ticker, timeSet, limit=(rollingSize * 2)).df
    HighVol =  stock[ticker].drop(['open','high','low'], axis = 1)
    std = HighVol['close'].rolling(rollingSize).std()
    return std

def LastTransaction():
  LastActionQTY = api.get_activities()[0].qty
  LastActionSym = api.get_activities()[0].symbol
  LastActionPrice = api.get_activities()[0].price
  TotalAAPrice = int(float(LastActionPrice) * float(LastActionQTY))
  return print(f'Sold {LastActionSym} at {LastActionPrice} X {LastActionQTY} = {TotalAAPrice} ')

def BuyPercentage(stock,percentOfAccount = 1.0):

  api.cancel_all_orders()
  # Get total open trading value
  account = api.get_account()
  liquid = float(account.buying_power)
  liquid *= percentOfAccount

  # This will return the total value
  asset_df = api.get_barset(stock,'minute',limit=1).df
  asset_value = asset_df[stock]['high'][0]

  # to give some wiggle room on the orders adding a 2% buffer
  asset_value *= 1.02
  total_order_size = round(int( liquid / asset_value))
  if (total_order_size > 0):
    api.submit_order(stock,
                  side='buy', 
                  qty=total_order_size,
                  type='market',
                  time_in_force='day')
    print(f'Buying {total_order_size} of {stock} at {asset_value} for a total of {total_order_size * asset_value}')
  else:
    print(f"You ain't got money honey ${liquid} for {stock} @ ${asset_value}")
  
  # https://docs.alpaca.markets/trading-on-alpaca/orders/


def SellPercentage(stock,percent = 1.0):
  
  api.cancel_all_orders()
  # Get current stocks
  positionSize = api.get_position(stock).qty

  saleQty = int(float(positionSize) * percent)

  api.submit_order(stock,
                  side='sell', 
                  qty=saleQty,
                  type='market',
                  time_in_force='day')
  # https://docs.alpaca.markets/trading-on-alpaca/orders/

def GTFO():
  api.cancel_all_orders()
  api.close_all_positions()

def GetStockQty(stock):
  try:
    stockQty = int(api.get_position(stock).qty)
  except:
    print(f'There are none of this stock {stock}')
    stockQty = 0
  return stockQty