import os
import mysql.connector
import json

# testing
try:
    import binanceApiFunctions as baf
except:
    print("Error importing binance api functions! <br>")

try:
    baf.initialise(os.environ.get('API_KEY'), os.environ.get('SECRET_KEY'))
except:
    print("Error initializing keys.<br>")

try:
    cnx = mysql.connector.connect(
        user=os.environ.get('USER'),
        password=os.environ.get('PASS'),
        host=os.environ.get('HOST'),
        database=os.environ.get('DATABASE')
    )
    mycursor = cnx.cursor()
except:
    print("Error connecting to database. <br>")

def storeAccountData():
    data = baf.getUsrAccountData()
    accounts = {}
    for d in data["balances"]:
        tempAccount = {}
        tempAccount["free"] = d["free"]
        tempAccount["locked"] = d["locked"]
        tempAccount["total"] = str(float(d["free"])+float(d["locked"]))
        accounts[d["asset"]] = tempAccount
    accounts = json.dumps(accounts)
    user_id = 14
    exch_id = 10
    done = False
    while(not done):
        mycursor.execute(f"SELECT `id` FROM user_account WHERE `user_id`=14 AND `exch_id`=10")
        for x in mycursor:
            if (type(x[0] == int)):
                id = x[0]
                sqlUpdate = (f"UPDATE user_account SET `docs`='{accounts}' WHERE `id`={id}")
                mycursor.execute(sqlUpdate)
                done = True
                break
        if (done): break
        mycursor.reset()
        sqlInsert = (f"INSERT INTO user_account (`user_id`, `exch_id`, `docs`) VALUES ({user_id}, {exch_id}, '{accounts}')")
        mycursor.execute(sqlInsert)
        cnx.commit()
        break

    mycursor.close()
    cnx.close()

try:
    storeAccountData()
except:
    print("Error storing account data.")