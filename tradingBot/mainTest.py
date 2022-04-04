import binanceApiFunctions as baf
import TradingBot as tb
import time
from dotenv import load_dotenv
import testFunctions as test
import os

load_dotenv()
baf.initialise(os.environ.get("API_KEY"), os.environ.get("SECRET_KEY"))

# starting data
token1 = 'BTC'
token2 = 'USD'
tradePair = token1+token2
interval = "1h"
amount = 100
tradeFee = 0.99925  # fee per trade multiplier

# tests connections and structure
def testRun():
    """Testing the connections and structure"""
    print("\n\nTesting the Binance API connections:\nTesting . . .\n")
    test.testConn()
    time.sleep(5)
    print("\n\nTesting the Binance API Order Requests:\nTesting . . .\n")
    test.testOrder(tradePair)
    time.sleep(5)
    print("\n\nTesting the Binance API get Kline Request:\nTesting . . .\n")
    test.testGetKlines(tradePair, interval)
    time.sleep(5)
    print("\n\nTesting the converting Kline data into Pandas DataFrame:\nTesting . . .\n")
    test.testGetData(tradePair, interval)
    time.sleep(5)

    # Testing the Trading Bot class
    print("\n\nTesting the Trading Bot structure:\nTesting . . .\n")
    testBot = tb.TradingBot(amount, token1, token2, tradeFee, interval)
    testBot.test()
    time.sleep(10)

    # Uncomment to test running loop
    print("\n\nTesting the Trading Bot loop structure:\nTesting . . .\n")
    test.testBotLoop(token1, token2, interval)
    
if __name__ == "__main__":
    testRun()