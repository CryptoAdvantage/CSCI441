

#import os
#import urllib.parse
import sys
try:
    import TradingBot as tb
except:
    print("Error importing TradingBot class! <br>")

try:
    import binanceApiFunctions as baf
except:
    print("Error imprting binance api functions! <br>")

try:
    print("<h3>Inside of Python</h3>")
    print("Var1 within Python= ", sys.argv[1], "<br>")
    print("Var2 within Python= ", sys.argv[2], "<br>")
    print("Var3 within Python= ", sys.argv[3], "<br>")
    print("Var4 within Python= ", sys.argv[4], "<br>")
    print("Var5 within Python= ", sys.argv[5], "<br>")
    print("Var6 within Python= ", sys.argv[6], "<br>")
except:
    print("Error printing variables.")

try:
    botName = sys.argv[1]
    exchange = sys.argv[2]
    token1 = sys.argv[3]
    token2 = sys.argv[4]
    interval = sys.argv[5]
    strategy = sys.argv[6]
except:
    print("Error storing variables.")

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
