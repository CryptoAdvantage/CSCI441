""" from datetime import datetime as dt
import time
import binanceApiFunctions as baf
import pandas as pd
import talib as tal
from ta import add_all_ta_features
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pickle


def bollinger_bands(data, sma, window, nstd):
    "Return upper and lower Bollinger Bands."
    std = data.rolling(window=window).std()
    upper_band = sma + std * nstd
    lower_band = sma - std * nstd
    return upper_band, lower_band

def sma(data, window):
    "Return rolling mean of given values, using specified window size."
    return data.rolling(window = window).mean()

def bb_simple(df, bot):
    for i in range(len(df)):
        if bot.curr_token == 'USD':
            if df['low'].iloc[i] < df['lowerBand'].iloc[i]: # buy signal
                bot.buy('BTC', df['lowerBand'].iloc[i], df['closeTime'].iloc[i])
                break
        if bot.curr_token != 'USDT':
            if df['high'].iloc[i] > df['upperBand'].iloc[i]: # sell signal
                bot.sell('BTC', df['upperBand'].iloc[i], df['closeTime'].iloc[i])
                break
            
    print(f'num buys: {len(bot.buys)}  buys: {bot.buys}')
    print(f'num sells: {len(bot.sells)}')
    print(f'ending balance: {bot.amount} {bot.coin}') 

def bb_simple(bot):
    "loop framework"
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
    
def bb_double_bottom(df, bot):
    for i in range(len(df)):
        if bot.curr_token == 'USDT':
            if bot.bottom == 'hit' and df['low'].iloc[i] > df['lowerBand'].iloc[i]:
                bot.bottom = 'released'
            if df['low'].iloc[i] < df['lowerBand'].iloc[i]: # buy signal
                if bot.bottom == 'released':
                    bot.buy('BTC', df['lowerBand'].iloc[i], df['closeTime'].iloc[i])
                    bot.reset_bottom()
                    break
                else:
                    bot.bottom = 'hit'
        if bot.curr_token != 'USDT':
            if df['high'].iloc[i] > df['upperBand'].iloc[i]: # sell signal
                if bot.top == 'released':
                    bot.sell('BTC', df['upperBand'].iloc[i], df['closeTime'].iloc[i])
                    bot.reset_top()
                    break
                else:
                    bot.tops == 'hit'
                    
    print(f'num buys: {len(bot.buys)}  buys: {bot.buys}')
    print(f'num sells: {len(bot.sells)}')
    print(f'ending balance: {bot.amount} {bot.token}')
    
def save_pca(pca):
    pkl_filename = "pca_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(pca, file)
        
def load_pca(file_name):
    with open(file_name, 'rb') as file:
        pca = pickle.load(file)
        return pca
    
def ml_test(df, normed_cols):
    labels = []
    xs = []
    ys = []
    for i in range(len(df)):
        labels.append(df['open'].iloc[i] / df['close'].iloc[i])
    df = df.head(len(df))
    df['label'] = labels
    add_all_ta_features(df, open='open', high='high', low='low', close='close', volume='volume')
    df = df[50:].reset_index(drop=True).fillna(0)
    dfn = df[normed_cols]


    x = (dfn-dfn.min())/(dfn.max()-dfn.min())
    xs.append(x)
    y = df['label']
    ys.append(y)
    x = pd.concat(xs)
    y = pd.concat(ys)
    
    
    pca = PCA(n_components=2)
    pca.fit(x)
    pcas = pd.DataFrame(pca.transform(x),columns=['pca1','pca2'])
    pcas['label'] = list(y)
    
    #plt.scatter(pcas['pca1'], pcas['pca2']) """