try:
    import binanceApiFunctions as baf
except:
    print("Error importing binance api functions! <br>")
from datetime import datetime as dt
import time
import sys

print("<h3>Inside of Python tradingBot</h3>")
print(f"Sys path: {sys.path}")

class TradingBot:
    def __init__(self, balance, token1, token2, trade_fee, interval):
        self.key_data = baf.key_data
        self.balance = balance
        self.token = token1
        self.curr_token = token2
        self.trade_pair = token1+token2
        self.interval = interval
        self.buys = []
        self.sells = []
        self.trade_fee = trade_fee
        self.bottom = "none"
        self.top = "none"
        self.reset_bottom()
        self.reset_top()
        
    def buy(self, token, price, time):
        self.balance = (self.balance / price) * self.trade_fee
        #baf.marketBuyOrder(self.trade_pair, self.balance)    # Calls Binance Market Buy Order
        self.buy_test = baf.testNewOrder(self.trade_pair,"BUY","MARKET",quantity=1.0)
        self.buys.append([self.trade_pair, time, price, self.balance])
        self.token = self.curr_token
        self.curr_token = token
        
    def sell(self, token, price, time):
        self.balance = self.balance * price * self.trade_fee
        #baf.marketSellOrder(self.trade_pair, self.balance)   # Calls Binance Market Sell Order
        self.sell_test = baf.testNewOrder(self.trade_pair,"SELL","MARKET",quantity=1.0)
        self.sells.append([self.trade_pair, time, price, self.balance])
        self.token = self.curr_token
        self.curr_token = token
        
    def reset_bottom(self):
        self.bottom = 'none'
        
    def reset_top(self):
        self.top = 'none'

    def test(self):
        print('\nInitialized Bot:\n')
        print(f"balance: {self.balance}")
        print(f"Token: {self.token}")
        print(f"Current Token: {self.curr_token}")
        print(f"Trade Pair: {self.trade_pair}")
        print(f"Interval: {self.interval}")
        print(f"Buys List: {self.buys}")
        print(f"Sells List: {self.sells}")
        print(f"Trade Fee x: {self.trade_fee}")
        time.sleep(10)
        self.buy(self.token, 40000.0, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
        print("\n***After Buy Order***\n")
        print(f"balance: {self.balance}")
        print(f"Token: {self.token}")
        print(f"Current Token: {self.curr_token}")
        print(f"Buys List: {self.buys}")
        print(f"Sells List: {self.sells}")
        time.sleep(10)
        self.sell(self.token, 50000.0, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
        print("\n***After Sell Order***\n")
        print(f"balance: {self.balance}")
        print(f"Token: {self.token}")
        print(f"Current Token: {self.curr_token}")
        print(f"Buys List: {self.buys}")
        print(f"Sells List: {self.sells}")
        