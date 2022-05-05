import sys
import os
from datetime import datetime as dt
import time

try:
    import TradingBot as tb
except:
    print("Error importing TradingBot class! <br>")
try:
    import binanceApiFunctions as baf
except:
    print("Error imprting binance api functions! <br>")
""" try:
    import myModels
except:
    print("Error importing models <br>") """

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

def bb_simple(bot):
    """loop framework"""
    start = True
    current_token = bot.token2
    while True:
        if (dt.now().second % 10 == 0) or start:
            if (dt.now().minute % 2 == 0 and dt.now().second == 10) or start:
                start = False
                # refresh data
                df = baf.getData(bot.trade_pair, bot.interval)
                state = baf.getState(df)
            
            obPriceData = baf.getBestObPrice(bot.trade_pair)
            if current_token == bot.token2:
                askPrice = float(obPriceData['askPrice'])
                print(f"AskPrice: {askPrice}")
                lowerBand = df['lowerBand'].iloc[-1]
                print(f"Lower Band: {lowerBand}")
                if askPrice < lowerBand and state == 'between':
                    bot.buy(askPrice, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
                    current_token = bot.token1
                    break

            if current_token != bot.token2:
                bidPrice = float(obPriceData['bidPrice'])
                print(f"AskPrice: {askPrice}")
                upperBand = df['upperBand'].iloc[-1]
                print(f"Upper Band: {upperBand}")
                if bidPrice > upperBand and state == 'between':
                    bot.sell(bidPrice, dt.now().strftime("%d-%m-%Y  %I:%M%p"))
                    current_token = bot.token2
                    
        print(f"new loop - Time: {dt.now()}")
        time.sleep(1)

try:
    baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
    print(baf.testConnection())
    t_bot = tb.TradingBot(email, botName, strategy, exchange, amount, token1, token2, tradeFee, interval)
    #bb_simple(t_bot)
    print("Bot Active")
except:
    print("Error running bot.<br>")

try:
    print("<br><br><h3>Trading Bot Settings:</h3>")
    print("User Email: ", email, "<br>")
    print("Bot Name: ", botName, "<br>")
    print("Exchange: ", exchange, "<br>")
    print("Token 1: ", token1, "<br>")
    print("Token 2: ", token2, "<br>")
    print("Trading Pair: ", token1+token2, "<br>")
    print("Interval: ", interval, "<br>")
    print("Trading Strategy: ", strategy, "<br>")
    if (posted == "true"):
        print("Stored to DB <br>")
except:
    print("Error storing settings. <br>")