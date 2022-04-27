import binanceApiFunctions as baf
import requests
import json
import os

tradePair = "BTCUSD"
interval = "1h"

baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
url = 'https://csci441project.herokuapp.com/history.php'
klines = baf.getKlines(tradePair, internal=interval, limit=1000)
x = requests.post(url, json = json.dumps(klines))
print(x.text)