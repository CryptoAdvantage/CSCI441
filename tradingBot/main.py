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
    print("\n\nTesting the Binance API connections:\n\n")
    test.testConn()
    test.testOrder(tradePair)
    test.testGetKlines(tradePair, interval)
    test.testGetData(tradePair, interval)
    time.sleep(12)

    # Testing the Trading Bot class
    print("\n\nTesting the Trading Bot structure:\n\n")
    testBot = tb.TradingBot(amount, token1, token2, tradeFee, interval)
    testBot.test()
    time.sleep(20)

    # Uncomment to test running loop
    print("\n\nTesting the Trading Bot loop structure:\n\n")
    test.testBotLoop(token1, token2, interval)
    
      
if __name__ == "__main__":
    testRun()