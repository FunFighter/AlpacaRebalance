import alpaca_trade_api as alpaca


api = alpaca.REST('PKC2296SJUWCR0RL39TY','fztCve2EEUo/rNkRXIeRus/qtWOPT4sBjbhBaenR', 'https://paper-api.alpaca.markets')

def BuyPercentage(stock,percentOfAccount = 1.0):

  # Get total open trading value
  account = api.get_account()
  liquid = float(account.buying_power)
  print(f'{liquid} liquid value')
  liquid *= percentOfAccount
  
  # This will return the total value
  #api.get_position('QQQ')
  asset_df = api.get_barset(stock,'minute',limit=1).df
  asset_value = asset_df[stock]['high'][0]

  # to give some wiggle room on the orders adding a 2% buffer
  asset_value *= 1.02
  total_order_size = round(int( liquid / asset_value))
  print(f'{total_order_size} total order of {stock} at {asset_value}')
  
  api.submit_order(stock,
                  side='buy', 
                  qty=total_order_size,
                  type='market',
                  time_in_force='day')
  # https://docs.alpaca.markets/trading-on-alpaca/orders/

if (api.get_clock().is_open):
    # Clear pending orders before trading
    api.cancel_all_orders()
    BuyPercentage('TQQQ', 1.0)
else:
    print('The market is {}'.format('open.' if api.get_clock().is_open else 'closed.'))