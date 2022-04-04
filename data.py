import mysql.connector
import requests
import json 
import time
import config

def initialize():
    conn=mysql.connector.connect(host='localhost',port=int(3306),user='root',passwd=config.password,db=config.database)
    cursor = conn.cursor()
    return conn, cursor

#Code to extract a singular row of data -- not used when running program to collect data
def data_extraction_singular():
    #make use of config.py for API security
    response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={}".format(config.api_key))

    var = response.json()
    print(var)
    #extracting SafeGasPrice(slow), FastGasPrice (fast), ProposeGasPrice (average)
    low = var["result"]["SafeGasPrice"]
    fast = var["result"]["FastGasPrice"]
    average = var["result"]["ProposeGasPrice"]
    blockNum = var["result"]["LastBlock"]

def create_query(cursor):
    #create query to load data
    drop = "DROP TABLE IF EXISTS gas_data"
    cursor.execute(drop)
    create_query = "CREATE TABLE gas_data (time BIGINT, low BIGINT, fast BIGINT, average BIGINT, blockNum BIGINT)"
    cursor.execute(create_query)
    return cursor


def data_extract_continuous(cursor, conn):
    now = int( time.time() )
    next_time = now
    while(1): 
        now = int( time.time())
        #include to insert new data every second
        if next_time == now:
            next_time = next_time + 1
            response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={}".format(config.api_key))

            var = response.json()
            if var["message"] == "OK":
                #extracting SafeGasPrice(slow), FastGasPrice (fast), ProposeGasPrice (average)
                low = var["result"]["SafeGasPrice"]
                fast = var["result"]["FastGasPrice"]
                average = var["result"]["ProposeGasPrice"]
                blockNum = var["result"]["LastBlock"]

                #loading data into new query
                insert_query = "INSERT INTO gas_data (time, low, fast, average, blockNum) VALUES (%s, %s, %s, %s, %s)"
                val = (now, low, fast, average, blockNum)
                cursor.execute(insert_query, val)
                conn.commit()


if __name__ == "__main__":
    conn, cursor = initialize()
    print("Initialization complete")
    #data_extraction_singular()
    cursor = create_query(cursor)
    print("Database created")
    data_extract_continuous(cursor, conn)