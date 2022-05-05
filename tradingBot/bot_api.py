import sys
import os
import json
try:
    import requests
except:
    print("Error importing requests.")
try:
    import TradingBot as tb
except:
    print("Error importing TradingBot class! <br>")

try:
    import binanceApiFunctions as baf
except:
    print("Error imprting binance api functions! <br>")

try:
    import models
except:
    print("Error importing models")

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

""" try:
    user = 10
    botName = "Testing1"
    exchange = "binanceus"
    token1 = "BTC"
    token2 = "USD"
    interval = "1h"
    strategy = "BB"
    amount = 1000
    tradePair = token1+token2
    tradeFee = 0.99925
except:
    print("Error storing variables. <br>") """

""" try:
    #baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
    api = "CqQEHo0a1vY6BuoQKhL72B0nGzIjf2w8fKo0iTobJnpfLzaHfwgkZGVFzEb91kTG"
    sec = "FtX1LVJYGkKnauLBoirxuA13XVvSDug27QuC6bxcNpLdcm0R9RnzeLbAStFwLswH"
    baf.initialise(api, sec)
    print(baf.testConnection())
    t_bot = tb.TradingBot(user, botName, strategy, exchange, amount, token1, token2, tradeFee, interval)
    models.bb_simple(t_bot)
except:
    print("Error running bot.<br>") """

try:
    print("<h3>Trading Bot Settings:</h3>")
    print("User Email: ", email, "<br>")
    print("Bot Name: ", botName, "<br>")
    print("Exchange: ", exchange, "<br>")
    print("Token 1: ", token1, "<br>")
    print("Token 2: ", token2, "<br>")
    print("Trading Pair: ", token1+token2, "<br>")
    print("Interval: ", interval, "<br>")
    print("Trading Strategy: ", strategy, "<br>")
    if (posted == "true"):
        print("Store to DB")
except:
    print("Error printing variables. <br>")