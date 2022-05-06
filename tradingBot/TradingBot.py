try:
    import binanceApiFunctions as baf
except:
    print("Error importing binance api functions! <br>")
from datetime import datetime as dt

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

def store_trade(self, price, time):
        try:
            cnx = mysql.connector.connect(
                user=os.environ.get('USER'),
                password=os.environ.get('PASS'),
                host=os.environ.get('HOST'),
                database=os.environ.get('DATABASE')
            )
            mycursor = cnx.cursor()
        except:
            print("Error connecting to database. <br>")


        try:
            cmd = "SELECT `id` FROM tradepair WHERE `PairTicker`= %s"
            mycursor.execute(cmd, self.trade_pair)
            cnx.commit()
            tradepairID = mycursor.fetchone()

            cmd = "SELECT `id` FROM exchange WHERE `Name`= %s"
            mycursor.execute(cmd, self.exchange)
            cnx.commit()
            exchangeID = mycursor.fetchone()

            cmd = "SELECT `id` FROM cryptocurrency WHERE `Name`= %s"
            mycursor.execute(cmd, self.token2)
            cnx.commit()
            cryptoID = mycursor.fetchone()

            cmd = "INSERT INTO pricehistory (`CryptoID`, `Date`, `USD_Price`) VALUES (%s, %s, %s)"
            mycursor.execute(cmd, cryptoID, time, price)
            cnx.commit()
            priceID = mycursor.lastrowid()

            cmd = "INSERT INTO tradehistory (`PairID`, `ExchID`, `UserID`, `PriceID`, `Action`, `Quantity`) VALUES (%s, %s, %s, %s, %s, %s)"
            mycursor.execute(cmd, tradepairID, exchangeID, self.user, priceID, '0', self.amount)
            cnx.commit()

            mycursor.close()
            cnx.close()

        except:
            print("Error storing trade data.<br>")

    def test(self):
        print('<br>Initialized Bot: <br>')
        print(f"balance: {self.balance}<br>")
        print(f"Token: {self.token}<br>")
        print(f"Current Token: {self.curr_token}<br>")
        print(f"Trade Pair: {self.trade_pair}<br>")
        print(f"Interval: {self.interval}<br>")
        print(f"Buys List: {self.buys}<br>")
        print(f"Sells List: {self.sells}<br>")
        print(f"Trade Fee x: {self.trade_fee}<br>")
        self.buy(self.token, 40000.0, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
        print("<br>***After Buy Order***<br>")
        print(f"balance: {self.balance}<br>")
        print(f"Token: {self.token}<br>")
        print(f"Current Token: {self.curr_token}<br>")
        print(f"Buys List: {self.buys}<br>")
        print(f"Sells List: {self.sells}<br>")
        self.sell(self.token, 50000.0, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
        print("<br>***After Sell Order***<br>")
        print(f"balance: {self.balance}<br>")
        print(f"Token: {self.token}<br>")
        print(f"Current Token: {self.curr_token}<br>")
        print(f"Buys List: {self.buys}<br>")
        print(f"Sells List: {self.sells}<br>")
