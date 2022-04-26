"""
    Functions list for Binance US API Trading Bot
"""

import sys
sys.path.insert(0, '/home/hammock/anaconda3/lib/python3.9/site-packages')
try:
    import hashlib
except:
    print("Error importing hashlib module! <br>")

try:
    import hmac
except:
    print("Error importing hmac module! <br>")

try:
    import pandas as pd
except:
    print("Error importing Pandas! <br>")

try:
    import logging
except:
    print("Error imprting logging! <br>")

""" try:
    from tkinter import END
except:
    print("Error importing tkinter! <br>") """

try:
    import time
except:
    print("Error importing time! <br>")
try:
    import requests
except:
    print("Error importing requests module! <br>")

try:
    from urllib.parse import urlencode
except:
    print("Error importing urlencode! <br>")

try:
    from datetime import datetime as dt
except:
    print("Error importing datetime module! <br>")

try:
    import TALIB as tal
except:
    print("Error importing talib! <br>")


print("<h3>Inside of Python binanceApiFunctions</h3>")
print(f"Sys path: {sys.path}")

""" try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode """

key_data = {}

ENDPOINT = "https://api.binance.us"

cols = ["openTime",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "closeTime",
        "quoteVolume",
        "numTrades",
        "TBBAV",
        "TBQAV",
        "ignore"
]

normed_cols = ['volume_cmf',
               'volume_mfi',
               'volatility_dcp',
               'trend_psar_down_indicator',
               'trend_psar_up_indicator',
               'trend_stc',
               'momentum_rsi',
               'momentum_stoch_rsi',
               'momentum_stoch_rsi_k',
               'momentum_stoch_rsi_d',
               'momentum_stoch'
]

logger = logging.getLogger("Trading_bot")
hdlr = logging.FileHandler('tradingbot.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info("Imports completes and logger initialised")  # logger.error("Imports completes and logger initialised")

def initialise(apiKey, secret):
    """ Function: Initializes and stores apiKey and secretKey
        ------
        Params: apiKey, secret"""
    key_data["apiKey"] = apiKey
    key_data["secret"] = secret

def request(method, path, params=None):
    """ Function: Creates an unsigned request
        ------
        Params: method, path, params
        ------
        RETURNS: Response for unsigned request"""
    resp = requests.request(method=method, url=ENDPOINT + path, params=params)
    data = resp.json()
    if "msg" in data:
        logger.warning(data['msg'])
    return data

def getData(symbol,interval):
    """Returns a DataFrame object of requested data"""
    klines = getKlines(symbol, internal=interval)
    df = pd.DataFrame(klines, columns=cols)
    df.openTime = [dt.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M') for ts in df['openTime']]
    df.closeTime = [dt.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M') for ts in df['closeTime']]
    df.openTime = pd.to_datetime(df.openTime)
    df.closeTime = pd.to_datetime(df.closeTime)
    del df['ignore']
    for col in df.columns:
        if not 'Time' in col:
            df[col] = df[col].astype(float)
    df['sma'] = tal.SMA(df['close'], timeperiod=20)
    df['upperBand'], df['middleBand'], df['lowerBand'] = tal.BBANDS(df['close'], 20,2,2,0)
    return df

def getState(df):
    """Returns if the close price is below, above, or inbetween the bollinger bands"""
    state = ''
    if df['close'].iloc[-1] < df['lowerBand'].iloc[-1]:
        state = 'below'
    elif df['close'].iloc[-1] > df['upperBand'].iloc[-1]:
        state = 'above'
    else:
        state = 'between'
    return state

# Get candlestick data
def getKlines(symbolPair, internal, **kwargs):
    """ Function: Requests candlestick data
        ------
        Params: symbol, interval, startTime, endTime, limit
        ------
        RETURNS: Response for candlestick data request"""
    params = {"symbol": symbolPair, "interval": internal}
    params = {**params, **kwargs}
    data = request("GET", "/api/v3/klines", params)
    return [{
        "openTime": d[0],
        "open": d[1],
        "high": d[2],
        "low": d[3],
        "close": d[4],
        "volume": d[5],
        "closeTime": d[6],
        "quoteVolume": d[7],
        "numTrades": d[8],
        "takerBuyBaseAssetVol": d[9],
        "takerBuyQuoteAssetVol": d[10]
    } for d in data]

def signedRequest(method, path, params):
    """ Function: Creates a signed request
        ------
        Params: method, path, params
        ------
        RETURNS: Response for signed request"""
    """ if "apiKey" not in key_data or "secret" not in key_data:
        raise ValueError("Api key and secret key must be set") """
    query = urlencode(params, doseq=True)
    query += f"&timestamp={int(round(time.time() * 1000))}"
    secret = bytes(key_data["secret"], ("UTF-8"))
    signature = hmac.new(secret, query.encode("UTF-8"), hashlib.sha256).hexdigest()
    query += f"&signature={signature}"
    resp = requests.request(method, ENDPOINT + path + "?" + query,
                            headers={"X-MBX-APIKEY": key_data["apiKey"]})
    data = resp.json()
    if "msg" in data:
        logger.warning(data['msg'])
        # generate log that there was a problem
    return data

"""
    POST Order Parameters List:
    *** Name	            Type	Mandatory	Description

        symbol	            STRING	    YES	    Order trading pair (e.g., BTCUSD, ETHUSD)
        side	            ENUM	    YES	    Order side (e.g., BUY, SELL)
        type	            ENUM	    YES	    Order type (e.g., LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER)
        timeInForce	        ENUM	    NO	
        quantity	        DECIMAL	    NO	
        quoteOrderQty	    DECIMAL	    NO	
        price	            DECIMAL	    NO	    Order price
        newClientOrderId	STRING	    NO	    A unique ID among open orders. Automatically generated if not sent.
                                                Orders with the same newClientOrderID can be accepted only when the 
                                                previous one is filled, otherwise the order will be rejected.
        stopPrice	        DECIMAL	    NO	    Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        icebergQty	        DECIMAL	    NO	    Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        newOrderRespType	ENUM	    NO	    Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to FULL; all other orders default to ACK.
        recvWindow	        LONG	    NO	    The value cannot be greater than 60000
        timestamp	        LONG	    YES


    *** Type	            Additional Mandatory Parameters

        LIMIT	            timeInForce, quantity, price	
        MARKET	            quantity or quoteOrderQty
        STOP_LOSS	        quantity, stopPrice
        STOP_LOSS_LIMIT	    timeInForce, quantity, price, stopPrice
        TAKE_PROFIT	        quantity, stopPrice
        TAKE_PROFIT_LIMIT	timeInForce, quantity, price, stopPrice
        LIMIT_MAKER	        quantity, price
        
        
"""
# Test New Order
def testNewOrder(symbolPair, side, type, **kwargs):
    """ Function: Tests a new order
        ------
        Mandatory Params: symbol, side, type
        Nonmandatory Params: timeInForce, quantity, quoteOrderQty, price, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for order request"""
    params = {
        "symbol": symbolPair,
        "side": side,
        "type": type
    }
    params = {**params, **kwargs}
    path = "/api/v3/order/test"
    data = signedRequest("POST", path, params)
    return data

# Create Market Buy Order
def marketBuyOrder(symbolPair, assetAmount=None, pairAmount=None, **kwargs):
    """ Function: Creates a new Market Buy Order Request
        ------
        Mandatory Params: symbol, side, type, [quantity, or quoteOrderQty]
        Nonmandatory Params: timeInForce, price, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "MARKET",
        "quantity": formatNumber(assetAmount),
        "quoteOrderQty": formatNumber(pairAmount)
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Limit Buy Order
def limitBuyOrder(symbolPair, timeInForce, assetAmount, limitPrice, **kwargs):
    """ Function: Creates new Limit Buy Order Request
        ------
        Mandatory Params: symbol, side, type, timeInForce, quantity, price
        Nonmandatory Params: quoteOrderQty, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": timeInForce,
        "quantity": formatNumber(assetAmount),
        "price": limitPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Stop Loss Buy Order
def stopLossBuyOrder(symbolPair, assetAmount, stopPrice, **kwargs):
    """ Function: Creates new Stop Loss Buy Order Request
        ------
        Mandatory Params: symbol, side, type, quantity, stopPrice
        Nonmandatory Params: timeInForce, quoteOrderQty, newClientOrderId, price, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "STOP_LOSS",
        "quantity": formatNumber(assetAmount),
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Stop Loss Limit Buy Order
def stopLossLimitBuyOrder(symbolPair, timeInForce, assetAmount, limitPrice, stopPrice, **kwargs):
    """ Function: Creates new Stop Loss Limit Buy Order Request
        ------
        Mandatory Params: symbol, side, type, timeInForce, quantity, price, stopPrice
        Nonmandatory Params: quoteOrderQty, newClientOrderId, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "STOP_LOSS_LIMIT",
        "timeInForce": timeInForce,
        "quantity": formatNumber(assetAmount),
        "price": limitPrice,
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Take Profit Buy Order
def takeProfitBuyOrder(symbolPair, assetAmount, stopPrice, **kwargs):
    """ Function: Creates new Take Profit Buy Order Request
        ------
        Mandatory Params: symbol, side, type, quantity, stopPrice
        Nonmandatory Params: timeInForce, quoteOrderQty, newClientOrderId, price, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "TAKE_PROFIT",
        "quantity": formatNumber(assetAmount),
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Take Profit Limit Buy Order
def takeProfitLimitBuyOrder(symbolPair, timeInForce, assetAmount, limitPrice, stopPrice, **kwargs):
    """ Function: Creates new Take Profit Limit Buy Order Request
        ------
        Mandatory Params: symbol, side, type, timeInForce, quantity, price, stopPrice
        Nonmandatory Params: quoteOrderQty, newClientOrderId, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "TAKE_PROFIT_LIMIT",
        "timeInForce": timeInForce,
        "quantity": formatNumber(assetAmount),
        "price": limitPrice,
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Limit Maker Buy Order
def limitMakerBuyOrder(symbolPair, assetAmount, limitPrice, **kwargs):
    """ Function: Creates new Limit Maker Buy Order Request
        ------
        Mandatory Params: symbol, side, type, quantity, price
        Nonmandatory Params: timeInForce, quoteOrderQty, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "BUY",
        "type": "LIMIT_MAKER",
        "quantity": formatNumber(assetAmount),
        "price": limitPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Market Sell Order
def marketSellOrder(symbolPair, assetAmount=None, pairAmount=None, **kwargs):
    """ Function: Creates a new Market Sell Order Request
        ------
        Mandatory Params: symbol, side, type, [quantity, or quoteOrderQty]
        Nonmandatory Params: timeInForce, price, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "MARKET",
        "quantity": formatNumber(assetAmount),
        "quoteOrderQty": pairAmount
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Limit Sell Order
def limitSellOrder(symbolPair, timeInForce, assetAmount, limitPrice, **kwargs):
    """ Function: Creates new Limit Sell Order Request
        ------
        Mandatory Params: symbol, side, type, timeInForce, quantity, price
        Nonmandatory Params: quoteOrderQty, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "LIMIT",
        "timeInForce": timeInForce,
        "quantity": formatNumber(assetAmount),
        "price": limitPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Stop Loss Sell Order
def stopLossSellOrder(symbolPair, assetAmount, stopPrice, **kwargs):
    """ Function: Creates new Stop Loss Sell Order Request
        ------
        Mandatory Params: symbol, side, type, quantity, stopPrice
        Nonmandatory Params: timeInForce, quoteOrderQty, newClientOrderId, price, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "STOP_LOSS",
        "quantity": formatNumber(assetAmount),
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Stop Loss Limit Sell Order
def stopLossLimitSellOrder(symbolPair, timeInForce, assetAmount, limitPrice, stopPrice, **kwargs):
    """ Function: Creates new Stop Loss Limit Sell Order Request
        ------
        Mandatory Params: symbol, side, type, timeInForce, quantity, price, stopPrice
        Nonmandatory Params: quoteOrderQty, newClientOrderId, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "STOP_LOSS_LIMIT",
        "timeInForce": timeInForce,
        "quantity": formatNumber(assetAmount),
        "price": limitPrice,
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Take Profit Sell Order
def takeProfitSellOrder(symbolPair, assetAmount, stopPrice, **kwargs):
    """ Function: Creates new Take Profit Sell Order Request
        ------
        Mandatory Params: symbol, side, type, quantity, stopPrice
        Nonmandatory Params: timeInForce, quoteOrderQty, newClientOrderId, price, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "TAKE_PROFIT",
        "quantity": formatNumber(assetAmount),
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Take Profit Limit Sell Order
def takeProfitLimitSellOrder(symbolPair, timeInForce, assetAmount, limitPrice, stopPrice, **kwargs):
    """ Function: Creates new Take Profit Limit Sell Order Request
        ------
        Mandatory Params: symbol, side, type, timeInForce, quantity, price, stopPrice
        Nonmandatory Params: quoteOrderQty, newClientOrderId, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "TAKE_PROFIT_LIMIT",
        "timeInForce": timeInForce,
        "quantity": formatNumber(assetAmount),
        "price": limitPrice,
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Create Limit Maker Sell Order
def limitMakerSellOrder(symbolPair, assetAmount, limitPrice, **kwargs):
    """ Function: Creates new Limit Maker Sell Order Request
        ------
        Mandatory Params: symbol, side, type, quantity, price
        Nonmandatory Params: timeInForce, quoteOrderQty, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow, timestamp
        ------
        RETURNS: Response for creation request"""
    params = {
        "symbol": symbolPair,
        "side": "SELL",
        "type": "LIMIT_MAKER",
        "quantity": formatNumber(assetAmount),
        "price": limitPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("POST", path, params)
    return data

# Get Order
def getOrder(symbolPair, orderId=None, origClientOrderId=None, **kwargs):
    """ Function: Requests trade order's status by orderId or origClientOrderId
        ------
        Mandatory Params: symbol, [orderId or origClientOrderId], timestamp
        Nonmandatory Params: recvWindow 
        ------
        RETURNS: Response for request for a trade order's status"""
    params = {
        "symbol": symbolPair,
        "orderId": orderId,
        "origClientOrderId": origClientOrderId
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("GET", path, params)
    return data

# Get All Open Orders
def getAllOpenOrders(**kwargs):
    """ Function: Requests all open trade orders on a token symbol. Do not access this without a token symbol as this would return all pair data.
        ------
        Mandatory Params: timestamp 
        Nonmandatory Params: symbol, recvWindow
        ------
        RETURNS: Response for request for all open trade orders"""
    params = {**kwargs}
    path = "/api/v3/openOrders"
    data = signedRequest("GET", path, params)
    return data

# Cancel Order
def cancelOrder(symbolPair, orderId=None, origClientOrderId=None, **kwargs):
    """ Function: Cancels an active trade order and returns response
        ------
        Mandatory Params: symbol, timestamp
        Nonmandatory Params: orderId, origClientOrderId, newClientOrderId, recvWindow 
        ------
        RETURNS: Response from canceled trade order"""
    params = {
        "symbol": symbolPair,
        "orderId": orderId,
        "origClientOrderId": origClientOrderId
    }
    params = {**params, **kwargs}
    path = "/api/v3/order"
    data = signedRequest("DELETE", path, params)
    return data

# Cancel Open Orders for Symbol
def cancelOpenOrdersForSymbol(symbolPair, orderId=None, origClientOrderId=None, **kwargs):
    """ Function: Cancels an active trade order
        ------
        Mandatory Params: symbol, timestamp
        Nonmandatory Params: recvWindow 
        ------
        RETURNS: Response from canceled trade order"""
    params = {"symbol": symbolPair}
    params = {**params, **kwargs}
    path = "/api/v3/openOrders"
    data = signedRequest("DELETE", path, params)
    return data

# Get Trades
def getTrades(symbolPair, **kwargs):
    """ Function: get trade data for a specific account and token symbol.
        ------
        Mandatory Params: symbol, timestamp
        Nonmandatory Params: orderId, startTime, endTime, fromId, limit, recvWindow
        ------
        RETURNS: Response for requested trade data for account or token symbol"""
    params = {"symbol": symbolPair}
    params = {**params, **kwargs}
    path = "/api/v3/myTrades"
    data = signedRequest("GET", path, params)
    return data

# Create new OCO Order
def createNewOcoOrder(symbolPair, side, quantity, price, stopPrice, **kwargs):
    """ Function: place a new OCO(one-cancels-the-other) order.
        ------
        Mandatory Params: symbol, side, quantity, price, stopPrice, timestamp 
        Nonmandatory Params: listCLientOrderId, limitClientOrderId, limitIcebergQty, stopClientOrderId, stopLimitPrice, 
                             stopIcebergQty, stopLimitTimeInForce, newOrderRespType, recvWindow
        ------
        RETURNS: Response for new OCO order"""
    params = {
        "symbol": symbolPair,
        "side": side,
        "quantity": quantity,
        "price": price,
        "stopPrice": stopPrice
    }
    params = {**params, **kwargs}
    path = "/api/v3/order/oco"
    data = signedRequest("POST", path, params)
    return data

# Get OCO Order
def getOcoOrder(orderListId=None, listClientOrderId=None, **kwargs):
    """ Function: retrieve a specific OCO order based on provided optional parameters.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: orderListId, origClientOrderId, recvWindow
        -------
        RETURNS: Response for retrieved OCO order"""
    params = {
        "orderListId": orderListId,
        "listClientOrderId": listClientOrderId
    }
    params = {**params, **kwargs}
    path = "/api/v3/orderList"
    data = signedRequest("GET", path, params)
    return data

# Get All OCO Orders
def getAllOcoOrders(**kwargs):
    """ Function: retrieves all OCO orders based on provided optional parameters. Please note the maximum limit is 1,000 orders.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: fromId, startTime, endTime, limit, recvWindow
        -------
        RETURNS: Response for retrieved OCO orders"""
    params = {**kwargs}
    path = "/api/v3/allOrderList"
    data = signedRequest("GET", path, params)
    return data

# Get Open OCO Orders
def getOpenOcoOrders(**kwargs):
    """ Function: retrieves all open OCO orders
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: recvWindow
        -------
        RETURNS: Response for retrieved OCO orders"""
    params = {**kwargs}
    path = "/api/v3/openOrderList"
    data = signedRequest("GET", path, params)
    return data

# Cancel OCO Order
def cancelOcoOrder(symbolPair, orderListId=None, listClientOrderId=None, **kwargs):
    """ Function: cancels an entire order list
        ------
        Mandatory Params: symbol, timestamp, [orderListId or listClientOrderId]
        Nonmandatory Params: newClientOrderId, recvWindow
        ------
        RETURNS: Response for cancelled OCO orders"""
    params = {
        "symbol": symbolPair,
        "orderListId": orderListId,
        "listClientOrderId": listClientOrderId
    }
    params = {**params, **kwargs}
    path = "/api/v3/orderList"
    data = signedRequest("DELETE", path, params)
    return data

# Get Supported Coin Pairs
def getSupportedCoinPairs(**kwargs):
    """ Function: retrieves a list of supported coin pairs for convert
        ------
        Params: fromCoin, toCoin
        ------
        RETURNS: Response for retrieved list"""
    params = {**kwargs}
    path = "/sapi/v1/otc/selectors"
    data = request("GET", path, params)
    return data

# Request for Quote
def requestForQuote(fromCoin, toCoin, requestCoin, requestAmount):
    """ Function: requests a quote for a from-to coin pair.
        ------
        Mandatory Params: fromCoin, toCoin, requestCoin, requestAmount
        ------
        RETURNS: Response for retrieved list"""
    params = {
        "fromCoin": fromCoin,
        "toCoin": toCoin,
        "requestCoin": requestCoin,
        "requestAmount": requestAmount
    }
    path = "/sapi/v1/otc/quotes"
    data = request("POST", path, params)
    return data

# Place OTC Trade Order
def placeOtcTradeOrder(quoteId):
    """ Function: places an order using an acquired quote.
        ------
        Mandatory Params: quoteId
        ------
        RETURNS: Response for placed order"""
    params = {"quoteId": quoteId}
    path = "/sapi/v1/otc/orders"
    data = request("POST", path, params)
    return data

# Get OTC Trade Order
def getOtcTradeOrder(orderId):
    """ Function: queries OTC trade order details.
        ------
        Mandatory Params: orderId
        ------
        RETURNS: Response for queried order"""
    path = "/sapi/v1/otc/orders/{orderId}"
    data = request("GET", path)
    return data

# Get all OTC Trade Orders
def getAllOtcTradeOrders(**kwargs):
    """ Function: queries OTC trade orders by condition.
        ------
        Nonmandatory Params: orderId, fromCoin, toCoin, startTime, endTime, limit
        ------
        RETURNS: Response for queried order"""
    params = {**kwargs}
    path = "/sapi/v1/orders"
    data = request("GET", path, params)
    return data

# Get Asset Fees & Wallet Status
def getAssetFees(**kwargs):
    """ Function: fetches the details of all crypto assets, including fees, withdrawal limits and network status.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: recvWindow
        ------
        RETURNS: Response for fetched data"""
    params = {**kwargs}
    path = "/sapi/v1/capital/config/getall"
    data = signedRequest("GET", path, params)
    return data

# Withdraw Crypto
def withdrawCrypto(symbol, network, address, amount, **kwargs):
    """ Function: submits a crypto withdrawal request.
        ------
        Mandatory Params: coin, network, address, amount, timestamp
        Nonmandatory Params: withdrawOrderId, addressTag, recvWindow
        ------
        RETURNS: Response for withdraw request"""
    params = {
        "coin": symbol,
        "network": network,
        "address": address,
        "amount": amount
    }
    params = {**params, **kwargs}
    path = "/sapi/v1/capital/withdraw/apply"
    data = signedRequest("POST", path, params)
    return data

# Withdraw Fiat
def withdrawFiat(paymentAccount, amount, **kwargs):
    """ Function: submits a USD withdraw request via Silvergate Exchange Network (SEN).
        ------
        Mandatory Params: paymentAccount, amount, timestamp
        Nonmandatory Params: paymentChannel, paymentMethod, fiatCurrency, recvWindow
        ------
        RETURNS: Response for withdraw request"""
    params = {
        "paymentAccount": paymentAccount,
        "amount": amount
    }
    params = {**params, **kwargs}
    path = "/sapi/v1/fiatpayment/apply/withdraw"
    data = signedRequest("POST", path, params)
    return data

# Get Crypto Withdraw History
def getCryptoWithdrawHistory(symbol, **kwargs):
    """ Function: fetches your crypto withdrawal history.
        ------
        Mandatory Params: coin, timestamp
        Nonmandatory Params: withdrawOrderId, status, startTime, endTime, offset, limit, recvWindow
        ------
        RETURNS: Response for request"""
    params = {"coin": symbol}
    params = {**params, **kwargs}
    path = "/sapi/v1/capital/withdraw/history"
    data = signedRequest("GET", path, params)
    return data

# Get Fiat Withdraw History
def getFiatWithdrawHistory(**kwargs):
    """ Function: fetches your fiat(USD) withdrawal history.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: fiatCurrency, orderId, offset, paymentChannel, paymentMethod,  startTime, endTime, recvWindow
        ------
        RETURNS: Response for request"""
    params = {**kwargs}
    path = "/sapi/v1/fiatpayment/query/withdraw/history"
    data = signedRequest("GET", path, params)
    return data

# Get Crypto Deposit Address
def getCryptoDepositAddress(symbol, **kwargs):
    """ Function: fetches a deposit address for a particular crypto asset.
        ------
        Mandatory Params: coin, timestamp
        Nonmandatory Params: network, recvWindow
        ------
        RETURNS: Response for request"""
    params = {"coin": symbol}
    params = {**params, **kwargs}
    path = "/sapi/v1/capital/deposit/address"
    data = signedRequest("GET", path, params)
    return data

# Get Crypto Deposit History
def getCryptoDepositHistory(symbol, **kwargs):
    """ Function: fetches your crypto deposit history.
        ------
        Mandatory Params: coin, timestamp
        Nonmandatory Params: status, startTime, endTime, offset, limit, recvWindow
        ------
        RETURNS: Response for request"""
    params = {"coin": symbol}
    params = {**params, **kwargs}
    path = "/sapi/v1/capital/deposit/hisrec"
    data = signedRequest("GET", path, params)
    return data

# Get Fiat Deposit History
def getFiatDepositHistory(**kwargs):
    """ Function: fetches your fiat(USD) deposit history.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: fiatCurrency, orderId, offset, paymentChannel, paymentMethod,  startTime, endTime, recvWindow
        ------
        RETURNS: Response for request"""
    params = {**kwargs}
    path = "/sapi/v1/fiatpayment/query/deposit/history"
    data = signedRequest("GET", path, params)
    return data

# Format number for exchange
def formatNumber(x):
    """ Function: Formats given number to float upto 8 decimal places
        ------
        Params: x - [int/float]
        ------
        RETURNS: Formatted x value"""
    if isinstance(x, float):
        return "{:.8f}".format(x)
    else:
        return str(x)

# To test connectivity
def testConnection():
    """ Function: tests connection to the api
        ------
        RETURNS: Response from tested connection"""
    conn = request("GET", "/api/v3/ping")
    return conn

# Get Server Time
def getServerTime():
    """ Function: gets the current server time.
        ------
        RETURNS: Response of current server time"""
    s_time = request("GET", "/api/v3/time")
    return s_time

# Get System Status
def getSystemStatus():
    """ Function: fetches the system status.
        ------
        RETURNS: Response of status request"""
    status = request("GET", "/wapi/v3/systemStatus.html")
    return status

# Get Exchange Information
def getExchangeInfo(**kwargs):
    """ Function: gets the current exchange trading rules and trading pair information.
        ------
        Params: symbol, symbols=symbol,symbol, symbols=["symbol","symbol"]
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/api/v3/exchangeInfo"
    info = request("GET", path, params)
    return info

# Get recent Trades
def getRecentTrades(symbolPair, **kwargs):
    """ Function: gets the recent trades. Please note the maximum limit is 1,000 trades.
        ------
        Mandatory Params: symbol
        Nonmandatory Params: limit
        ------
        RETURNS: Response for requested information"""
    params = {"symbol": symbolPair}
    params = {**params, **kwargs}
    path = "/api/v3/trades"
    trades = request("GET", path, params)
    return trades

# Get Historical Trades
def getHistTrades(symbolPair, **kwargs):
    """ Function: gets older trades. Please note the maximum limit is 1,000 trades.
        ------
        Mandatory Params: symbol
        Nonmandatory Params: limit, fromId
        ------
        RETURNS: Response for requested information"""
    params = {"symbol": symbolPair}
    params = {**params, **kwargs}
    path = "/api/v3/historicalTrades"
    trades = signedRequest("GET", path, params)
    return trades

# Get Aggregate Trades
def getAggTrades(symbolPair, **kwargs):
    """ Function: gets compressed, aggregate trades. Trades that fill at the time, from the same order, 
        with the same price will have the quantity aggregated. Please note the maximum limit is 1,000 trades.
        ------
        Mandatory Params: symbol
        Nonmandatory Params: fromId, startTime, endTime, limit
        ------
        RETURNS: Response for requested information"""
    params = {"symbol": symbolPair}
    params = {**params, **kwargs}
    path = "/api/v3/aggTrades"
    trades = request("GET", path, params)
    return trades

# Get Order Book Depth
def getObDepth(symbolPair, **kwargs):
    """ Function: gets the order book depth. Please note the limits in the table below.
        ------
        Mandatory Params: symbol
        Nonmandatory Params: limit
        ------
        RETURNS: Response for requested information"""
    params = {"symbol": symbolPair}
    params = {**params, **kwargs}
    path = "/api/v3/depth"
    depth = request("GET", path, params)
    return depth

# Get Live Ticker Price
def getLivePrice(**kwargs):
    """ Function: gets the latest price for a token symbol or symbols.
        ------
        NonMandatory Params: symbol
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/api/v3/ticker/price"
    price = request("GET", path, params)
    return price

# Get Average Price
def getAvgPrice(symbolPair):
    """ Function: gets the current average price for a symbol.
        ------
        Mandatory Params: symbol
        ------
        RETURNS: Response for requested information"""
    params = {"symbol": symbolPair}
    path = "/api/v3/avgPrice"
    price = request("GET", path, params)
    return price

# Get Best Order Book Price
def getBestObPrice(**kwargs):
    """ Function: gets the best price/qty on the order book for a token symbol or symbols.
        ------
        Nonmandatory Params: symbol
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/api/v3/ticker/bookTicker"
    price = request("GET", path, params)
    return price

# Get 24H Price Change Stats
def get24hPriceChange(**kwargs):
    """ Function: gets 24-hour rolling window price change statistics. Do not access this without a token symbol as this would return all pair data.
        ------
        Nonmandatory Params: symbol
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/api/v3/ticker/24hr"
    priceData = request("GET", path, params)
    return priceData

# Get User Account Data
def getUsrAccountData(**kwargs):
    """ Function: gets the users current account information
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/api/v3/account"
    accountData = signedRequest("GET", path, params)
    return accountData

# Get User Account Status
def getUsrAccountStatus(**kwargs):
    """ Function: fetches account status detail.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/wapi/v3/accountStatus.html"
    accountStatus = signedRequest("GET", path, params)
    return accountStatus

# Get User API Trading Status
def getUsrTradingStatus(**kwargs):
    """ Function: fetches account API trading status detail.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/wapi/v3/apiTradingStatus.html"
    tradingStatus = signedRequest("GET", path, params)
    return tradingStatus

# Get User Maker/Taker Rates
def getUsrMakerTakerRates(**kwargs):
    """ Function: fetches trading fess
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: symbol, recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/wapi/v3/tradeFee.html"
    rates = signedRequest("GET", path, params)
    return rates

# Get Asset Distribution History
def getAssetDistHistory(**kwargs):
    """ Function: queries asset distribution records, including for staking, referrals and airdrops etc.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: asset, startTime, endTime, recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/sapi/v3/asset/assetDividend.html"
    assetHistory = signedRequest("GET", path, params)
    return assetHistory

# Get Sub-account Information
def getSubAccountInfo(**kwargs):
    """ Function: fetches user sub-account list.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: email, status, page, limit, recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {**kwargs}
    path = "/wapi/v3/sub-account/list.html"
    accountInfo = signedRequest("GET", path, params)
    return accountInfo

# Get Sub-account Transfer History
def getSubAccountTransferHistory(email, **kwargs):
    """ Function: fetches user sub-account asset transfer history.
        ------
        Mandatory Params: email, timestamp
        Nonmandatory Params: startTime, endTime, page, limit, recvWindow
        ------
        RETURNS: Response for requested information"""
    params = {"email": email}
    params = {**params, **kwargs}
    path = "/wapi/v3/sub-account/transfer/history.html"
    accountHistory = signedRequest("GET", path, params)
    return accountHistory

# Execute Sub-account Transfer
def exeSubAccountTransfer(fromEmail, toEmail, asset, amount, **kwargs):
    """ Function: executes user sub-account asset transfers.
        ------
        Mandatory Params: fromEmail, toEmail, asset, amount, timestamp
        Nonmandatory Params: recvWindow
        ------
        RETURNS: Response for executed asset transfer"""
    params = {"fromEmail": fromEmail, "toEmail": toEmail, "asset": asset, "amount": amount}
    params = {**params, **kwargs}
    path = "/wapi/v3/sub-account/transfer.html"
    transfer = signedRequest("POST", path, params)
    return transfer

# Get Sub-account Assets
def getSubAccountAssets(email, **kwargs):
    """ Function: fetches user sub-account assets
        ------
        Mandatory Params: email, timestamp
        Nonmandatory Params: symbol, recvWindow
        ------
        RETURNS: Response for requested assets"""
    params = {"email": email}
    params = {**params, **kwargs}
    path = "/wapi/v3/sub-account/assets.html"
    assets = signedRequest("GET", path, params)
    return assets

# Get Order Rate Limits
def getOrderRateLimits(**kwargs):
    """ Function: Gets the current trade order count rate limits for all time intervals.
        ------
        Mandatory Params: timestamp
        Nonmandatory Params: recvWindow
        ------
        RETURNS: Response for requested data"""
    params = {**kwargs}
    path = "/api/v3/rateLimit/order"
    rateLimits = signedRequest("GET", path, params)
    return rateLimits