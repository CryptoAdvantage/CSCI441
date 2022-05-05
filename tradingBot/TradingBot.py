try:
    import binanceApiFunctions as baf
except:
    print("Error importing binance api functions! <br>")
from datetime import datetime as dt

class TradingBot:
    def __init__(self, user, botName, strategy, exchange, amount, token1, token2, trade_fee, interval):
        self.user = user
        self.name = botName
        self.strategy = strategy
        self.exchange = exchange
        self.key_data = baf.key_data
        self.amount = amount
        self.token1 = token1
        self.token2 = token2
        self.trade_pair = token1+token2
        self.interval = interval
        self.buys = []
        self.sells = []
        self.trade_fee = trade_fee
        self.bottom = "none"
        self.top = "none"
        self.reset_bottom()
        self.reset_top()
        
    def buy(self, price, time):
        self.amount = (baf.getUsrAccountData['balances'][self.token2] / price) * self.trade_fee
        baf.marketBuyOrder(self.trade_pair, self.balance1)    # Calls Binance Market Buy Order
        #self.buy_test = baf.testNewOrder(self.trade_pair,"BUY","MARKET",quantity=1.0)
        lastTrade = baf.getRecentTrades(self.trade_pair, 1)

        self.buys.append([self.trade_pair, time, price, self.balance1])
        
    def sell(self, price, time):
        self.balance = self.balance * price * self.trade_fee
        self.sells.append([self.trade_pair, time, price, self.balance1])
        baf.marketSellOrder(self.trade_pair, self.balance2)   # Calls Binance Market Sell Order
        #self.sell_test = baf.testNewOrder(self.trade_pair,"SELL","MARKET",quantity=1.0)
        
    def reset_bottom(self):
        self.bottom = 'none'
        
    def reset_top(self):
        self.top = 'none'

    def test(self):
        print('<br>Initialized Bot: <br>')
        print(f"balance: {self.balance}<br>")
        print(f"Token: {self.token1}<br>")
        print(f"Current Token: {self.token2}<br>")
        print(f"Trade Pair: {self.trade_pair}<br>")
        print(f"Interval: {self.interval}<br>")
        print(f"Buys List: {self.buys}<br>")
        print(f"Sells List: {self.sells}<br>")
        print(f"Trade Fee x: {self.trade_fee}<br>")
        self.buy(40000.0, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
        print("<br>***After Buy Order***<br>")
        print(f"balance: {self.balance}<br>")
        print(f"Token: {self.token1}<br>")
        print(f"Current Token: {self.token2}<br>")
        print(f"Buys List: {self.buys}<br>")
        print(f"Sells List: {self.sells}<br>")
        self.sell(50000.0, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
        print("<br>***After Sell Order***<br>")
        print(f"balance: {self.balance}<br>")
        print(f"Token: {self.token1}<br>")
        print(f"Current Token: {self.token2}<br>")
        print(f"Buys List: {self.buys}<br>")
        print(f"Sells List: {self.sells}<br>")
        