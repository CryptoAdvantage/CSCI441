import sys
import os

try:
    import binanceApiFunctions as baf
except:
    print("Error importing binance api functions! <br>")

try:
    exchange = sys.argv[1]
except:
    print("Error storing exchange variable. <br>")

try:
    baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
except:
    print("Error initializing keys.<br>")

""" try:
    DATABASE_URL=os.environ.get('JAWSDB_URL')
    print(DATABASE_URL)
except:
    print("Error connecting to database. <br>") """

try:
    data = baf.getUsrAccountData()
    print("Token &emsp; Available &emsp; Locked &emsp; Total<br>")
    for d in data["balances"]:
        asset = d["asset"]
        free = d["free"]
        locked = d["locked"]
        total = (float(free)+float(locked))
        total = str(total)
        print(f"{asset} &emsp; {free} &emsp; {locked} &emsp; {total}<br>")
except:
    print("Error getting account data.")