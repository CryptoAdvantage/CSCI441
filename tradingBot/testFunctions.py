import binanceApiFunctions as baf
from datetime import datetime as dt
import time

def testConn():
    """Testing the Binance API Connection"""
    conn = baf.testConnection()
    if(conn == {}):
        print("Successful Connection")
    else:
        print("Unsuccessful Connection")

def testOrder(symbolPair):
    """Testing the Binance API Order request"""
    marketBuy = baf.testNewOrder(symbolPair,"BUY","MARKET",quantity=1.0)
    marketSell = baf.testNewOrder(symbolPair,"SELL","MARKET",quantity=1.0)
    limitBuy = baf.testNewOrder(symbolPair,"BUY","LIMIT",timeInForce="GTC",quantity=1.0,price=10000.0)
    limitSell = baf.testNewOrder(symbolPair,"SELL","LIMIT",timeInForce="GTC",quantity=1.0,price=60000.0)
    testedOrders = [marketBuy, marketSell, limitBuy, limitSell]
    testedOrdersStr = ['Market Buy', 'Market Sell', 'Limit Buy', 'Limit Sell']
    for i in range(4):
        if testedOrders[i] == {}:
            print(f"{testedOrdersStr[i]} Successful!")
        else:
            print(f"{testedOrdersStr[i]} Unsuccessful.")

def testGetKlines(symbolPair, interval):
    """Testing the Binance API get klines request"""
    klines = baf.getKlines(symbolPair, internal=interval)
    if klines:
        print("Retrieve CandleStick Data Successful!")
    else:
        print("Retrieve CandleStick Data Unsuccessful.")

def testGetData(symbolPair, interval):
    """Testing retrieval and conversion of kline data into pandas DataFrame"""
    df = baf.getData(symbolPair, interval)
    if (len(df) == 0):
        print("Get Data as DataFrame Unsuccessful.")
    else:
        print("Get Data as DataFrame Successful!")

def testBotLoop(symbol1, symbol2, interval):
    """Testing the loop framework"""
    start = True
    current_token = symbol2
    while True:
        if (dt.now().second % 10 == 0) or start:
            if (dt.now().minute % 2 == 0 and dt.now().second == 10) or start:
                print("\nEntering get data cond***")
                start = False
                # refresh data
                df = baf.getData(symbol1+symbol2, interval)
                state = baf.getState(df)
                print(f'Current state of the market: {state}')
            
            print('\n')
            obPriceData = baf.getBestObPrice(symbol=symbol1+symbol2)
            if current_token == symbol2:
                print("Entering if buy cond***")
                askPrice = float(obPriceData['askPrice'])
                print(f"AskPrice: {askPrice}")
                lowerBand = df['lowerBand'].iloc[-1]
                print(f"Lower Band: {lowerBand}")
                if askPrice < lowerBand and state == 'between':
                    print("buy") # replace this line
                    current_token = symbol1
                    break

            if current_token != symbol2:
                print("Entering if sell cond***")
                bidPrice = float(obPriceData['bidPrice'])
                print(f"AskPrice: {askPrice}")
                upperBand = df['upperBand'].iloc[-1]
                print(f"Upper Band: {upperBand}")
                if bidPrice > upperBand and state == 'between':
                    print("sell") # replace this line
                    current_token = symbol2
                    
        print(f"new loop - Time: {dt.now()}")
        time.sleep(1)