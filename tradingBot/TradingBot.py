import binanceApiFunctions as baf
from datetime import datetime as dt

class TradingBot:
    def __init__(self, amount, token1, token2, trade_fee, interval):
        self.key_data = baf.key_data
        self.amount = amount
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
        self.amount = (self.amount / price) * self.trade_fee
        #baf.marketBuyOrder(self.trade_pair, self.amount)    # Calls Binance Market Buy Order
        self.buy_test = baf.testNewOrder(self.trade_pair,"BUY","MARKET",quantity=1.0)
        self.buys.append([self.trade_pair, time, price, self.amount])
        self.token = self.curr_token
        self.curr_token = token
        
    def sell(self, token, price, time):
        self.amount = self.amount * price * self.trade_fee
        #baf.marketSellOrder(self.trade_pair, self.amount)   # Calls Binance Market Sell Order
        self.sell_test = baf.testNewOrder(self.trade_pair,"SELL","MARKET",quantity=1.0)
        self.sells.append([self.trade_pair, time, price, self.amount])
        self.token = self.curr_token
        self.curr_token = token
        
    def reset_bottom(self):
        self.bottom = 'none'
        
    def reset_top(self):
        self.top = 'none'

    def test(self):
        print('\nInitialized Bot:\n')
        print(f"Amount: {self.amount}")
        print(f"Token: {self.token}")
        print(f"Current Token: {self.curr_token}")
        print(f"Trade Pair: {self.trade_pair}")
        print(f"Interval: {self.interval}")
        print(f"Buys List: {self.buys}")
        print(f"Sells List: {self.sells}")
        print(f"Trade Fee x: {self.trade_fee}")

        self.buy(self.token, 40000.0, dt.now())
        print("\n***After Buy Order***\n")
        print(f"Amount: {self.amount}")
        print(f"Token: {self.token}")
        print(f"Current Token: {self.curr_token}")
        print(f"Buys List: {self.buys}")
        print(f"Sells List: {self.sells}")

        self.sell(self.token, 50000.0, dt.now())
        print("\n***After Sell Order***\n")
        print(f"Amount: {self.amount}")
        print(f"Token: {self.token}")
        print(f"Current Token: {self.curr_token}")
        print(f"Buys List: {self.buys}")
        print(f"Sells List: {self.sells}")
        