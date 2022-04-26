

#import os
#import urllib.parse
import sys
import os
try:
    import TradingBot as tb
except:
    print("Error importing TradingBot class! <br>")

try:
    import binanceApiFunctions as baf
except:
    print("Error imprting binance api functions! <br>")

try:
    botName = sys.argv[1]
    exchange = sys.argv[2]
    token1 = sys.argv[3].upper()
    token2 = sys.argv[4].upper()
    interval = sys.argv[5]
    strategy = sys.argv[6]
    amount = 100
    tradeFee = 0.99925  # fee per trade multiplier
except:
    print("Error storing variables. <br>")

try:
    print("<h3>Inside of Python</h3>")
    print("Bot Name: ", botName, "<br>")
    print("Exchange: ", exchange, "<br>")
    print("Token 1: ", token1, "<br>")
    print("Token 2: ", token2, "<br>")
    print("Trading Pair: ", token1+token2, "<br>")
    print("Interval: ", interval, "<br>")
    print("Trading Strategy: ", strategy, "<br>")
except:
    print("Error printing variables. <br>")

try:
    baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
except:
    print("Error initializing api keys. <br>")

try:
    testBot = tb.TradingBot(amount, token1, token2, tradeFee, interval)
    testBot.test()
except:
    print("Error with Trading Bot. <br>")

""" print(botName)
print(exchange)
print(token1)
print(token2)
print(interval)
print(strategy) """
# startDate = ""
# endDate = ""

#test = tb.TradingBot(token1, token2, 0.99925, '1h')

#print(test.test())
