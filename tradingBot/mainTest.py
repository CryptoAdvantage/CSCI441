try:
    import TradingBot as tb
    #from .TradingBot import TradingBot
except:
    print("Error importing TradingBot.<br>")
try:
    import sys
except:
    print("Error importing sys.<br>")
try:
    import binanceApiFunctions as baf
except:
    print("Error importing binanceApiFunctions.<br>")

try:
    import testFunctions as test
except:
    print("Error importing testFunctions.<br>")
try:
    import os
except:
    print("Error importing os.<br>")

try:
    baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
except:
    print("Error initializing keys.<br>")

try:
    botName = sys.argv[1]
    exchange = sys.argv[2]
    token1 = sys.argv[3].upper()
    token2 = sys.argv[4].upper()
    interval = sys.argv[5]
    strategy = sys.argv[6]
    posted = sys.argv[7]
    email = sys.argv[8]
    amount = 1000
    tradeFee = 0.99925  # fee per trade multiplier
    tradePair = token1+token2
    if (strategy == 'bb'):
        strategy = 'Simple Bollinger Bands'
except:
    print("Error storing variables. <br>")

try:
    print("<h3>Inside of Python Main Test</h3>")
    print("Bot Name: ", botName, "<br>")
    print("Exchange: ", exchange, "<br>")
    print("Token 1: ", token1, "<br>")
    print("Token 2: ", token2, "<br>")
    print("Trading Pair: ", token1+token2, "<br>")
    print("Interval: ", interval, "<br>")
    print("Trading Strategy: ", strategy, "<br>")
except:
    print("Error printing variables. <br>")

# tests connections and structure
def testRun():
    """Testing the connections and structure"""
    print("<br><br>Testing the Binance API connections:<br>")
    test.testConn()
    print("<br><br>Testing the Binance API Order Requests:<br>")
    test.testOrder(tradePair)
    print("<br><br>Testing the Binance API get Kline Request:<br>")
    test.testGetKlines(tradePair, interval)
    print("<br><br>Testing the converting Kline data into Pandas DataFrame:<br>")
    test.testGetData(tradePair, interval)

    # Testing the Trading Bot class
    print("<br><br>Testing the Trading Bot structure:<br>")
    testBot = tb.TradingBot(email, botName, strategy, exchange, amount, token1, token2, tradeFee, interval)
    testBot.test()

    # Uncomment to test running loop
    #print("<br><br>Testing the Trading Bot loop structure:<br>")
    #test.testBotLoop(token1, token2, interval)

if __name__ == "__main__":
    testRun()
