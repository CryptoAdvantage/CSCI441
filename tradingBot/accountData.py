import sys
import os

try:
    import binanceApiFunctions as baf
except:
    print("Error imprting binance api functions! <br>")

try:
    exchange = sys.argv[1]
except:
    print("Error storing exchange variable. <br>")

try:
    baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
except:
    print("Error initializing keys.<br>")

try:
    data = baf.getUsrAccountData()
    print("Token     Available           Locked              Total<br>")
    for d in data["balances"]:
        asset = d["asset"]
        free = d["free"]
        locked = d["locked"]
        total = (float(free)+float(locked))
        total = str(total)
        print(asset.ljust(10)+free.ljust(20)+locked.ljust(20)+total.ljust(20)+"<br>")
except:
    print("Error getting account data.")