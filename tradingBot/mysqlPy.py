import mysql.connector
import os

DB_NAME = "nt84vrnvzds0ovdv"

def insertTable(table, columns, values, dbConn, cursor):
    sqlInsert = f"INSERT INTO {table} {columns} VALUES {values}"
    cursor.execute(sqlInsert)
    dbConn.commit()

def updateTable(table, setCol, setValue, whereCol, whereValue, dbConn, cursor):
    sqlUpdate = f"UPDATE {table} SET {setCol} = '{setValue}' WHERE {whereCol} = '{whereValue}'"
    cursor.execute(sqlUpdate)
    dbConn.commit()

def selectTable(table, selectCol, cursor):
    cursor.execute(f"SELECT {selectCol} FROM {table}")
    for x in cursor:
        print(x)

def deleteTable(table, whereCol, whereValue, dbConn, cursor):
    sqlDelete = f"DELETE FROM {table} WHERE {whereCol} = '{whereValue}'"
    cursor.execute(sqlDelete)
    dbConn.commit()

def createTable(table, tableData, cursor):
    sqlCreate = f"CREATE Table {table} {tableData}"
    cursor.execute(sqlCreate)

# for local development
cnx = mysql.connector.connect(
    user="faax40o0f0tzcrci",
    password="aeqnk4mlpsb6vohf",
    host="bv2rebwf6zzsv341.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    database="nt84vrnvzds0ovdv"
)

# For Heroku development
""" try:
    cnx = mysql.connector.connect(
        user=os.environ.get('USER'),
        password=os.environ.get('PASS'),
        host=os.environ.get('HOST'),
        database=os.environ.get('DATABASE')
    )
except:
    print("Error connecting to database. <br>") """