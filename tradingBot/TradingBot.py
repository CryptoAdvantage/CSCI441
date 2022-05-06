try:
    import binanceApiFunctions as baf
except:
    print("Error importing binance api functions! <br>")
from datetime import datetime as dt
try:
    import mysqlPy
except:
    print("Error importing mysqlPy functions <br>")

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
        self.trade_fee = trade_fee
        self.bottom = "none"
        self.top = "none"
        self.reset_bottom()
        self.reset_top()

    def buy(self, price, time):
        self.amount = (self.amount / price) * self.trade_fee
        baf.marketBuyOrder(self.trade_pair, self.amount)    # Calls Binance Market Buy Order
        #self.buy_test = baf.testNewOrder(self.trade_pair,"BUY","MARKET",quantity=1.0)
        try:
            values = (1, str(time), price)
            cols = f'(`CryptoID`, `Date`, `USD_Price`)'
            sqlInsert = f"INSERT INTO pricehistory {cols} VALUES {values}"
            botcursor = mysqlPy.cnx.cursor()
            botcursor.execute(f"USE {mysqlPy.DB_NAME}")
            botcursor.execute(sqlInsert)
            priceID = botcursor.lastrowid
            botcursor.reset()
        except:
            print("Error inserting pricehistory")
        try:
            values = (8, 10, 14, priceID, "BUY", self.amount)
            cols = f'(`PairID`, `ExchID`, `UserID`, `PriceID`, `Action`, `Quantity`)'
            sqlInsert = f"INSERT INTO tradehistory {cols} VALUES {values}"
            botcursor.execute(sqlInsert)
            mysqlPy.cnx.commit()
            botcursor.close()
            mysqlPy.cnx.close()
        except:
            print("Error inserting tradehistory")

    def sell(self, price, time):
        sellAmount = self.amount
        self.amount = self.amount * price * self.trade_fee
        baf.marketSellOrder(self.trade_pair, self.balance2)   # Calls Binance Market Sell Order
        #self.sell_test = baf.testNewOrder(self.trade_pair,"SELL","MARKET",quantity=1.0)
        try:
            values = (1, str(time), price)
            cols = f'(`CryptoID`, `Date`, `USD_Price`)'
            sqlInsert = f"INSERT INTO pricehistory {cols} VALUES {values}"
            botcursor = mysqlPy.cnx.cursor()
            botcursor.execute(f"USE {mysqlPy.DB_NAME}")
            botcursor.execute(sqlInsert)
            priceID = botcursor.lastrowid
            botcursor.reset()
        except:
            print("Error inserting pricehistory")
        try:
            values = (8, 10, 14, priceID, "SELL", sellAmount)
            cols = f'(`PairID`, `ExchID`, `UserID`, `PriceID`, `Action`, `Quantity`)'
            sqlInsert = f"INSERT INTO tradehistory {cols} VALUES {values}"
            botcursor.execute(sqlInsert)
            mysqlPy.cnx.commit()
            botcursor.close()
            mysqlPy.cnx.close()
        except:
            print("Error inserting tradehistory")

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
