from syslog import LOG_WARNING
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import config
import mysql.connector

#API initialization
app = Flask(__name__)
api = Api(app)

def initialize():
    #protect user password and database name through use of config file
    conn=mysql.connector.connect(host='localhost',port=int(3306),user='root',passwd=config.password,db=config.database)
    cursor = conn.cursor()
    return conn, cursor

class Users(Resource):
    def get(self):
        return {'data': 3}, 200

def receive_GET(cursor):
    recent_data = "SELECT low, fast, average, blockNum FROM gas_data WHERE time = (SELECT MAX(time) FROM gas_data)"
    cursor.execute(recent_data)
    #fetching most recent data
    return cursor.fetchone()

#first endpoint: /gas
@app.route('/gas', methods=['GET'])
def get_gas():
    conn, cursor = initialize()
    resp = receive_GET(cursor)
    output = {}
    output["low"] = resp[0]
    output["fast"] = resp[1]
    output["average"] = resp[2]
    output["blockNum"] = resp[3]
    return '{ "error": false, "message": ' + str(output) + '}'


def receive_GET_avg(cursor, fromTime, toTime):
    recent_data = "SELECT AVG(average) FROM gas_data WHERE time BETWEEN %s and %s"
    cursor.execute(recent_data, (fromTime, toTime))
    return cursor.fetchone()

#second endpoint: /average?fromTime=&toTime=
@app.route('/average', methods=['GET'])
def get_with_times():
    conn, cursor = initialize()
    fromTime = request.args.get('fromTime')
    #error handling
    if fromTime == None:
        return'{ "error": true, "message":  invalid request sent (fromTime) }'
    toTime = request.args.get('toTime')
    if toTime == None:
        return'{ "error": true, "message":  invalid request sent (toTime) }'

    #error handling - make sure times are digits and toTime >= fromTime
    if (toTime < fromTime or fromTime.isdigit() == False or toTime.isdigit() == False):
        return '{ "error": true, "message":  invalid UNIX timestamp(s) provided }'

    #error handling - make sure toTime doesn't go too far into future
    recent_data = "SELECT time FROM gas_data WHERE time = (SELECT MAX(time) FROM gas_data)"
    cursor.execute(recent_data)
    time = int(''.join(map(str, cursor.fetchone())))
    if int(toTime) > time:
        return '{ "error": true, "message": toTime is > latest UNIX time of available data }'
    resp = receive_GET_avg(cursor, fromTime, toTime)
    output = {}
    output["averageGasPrice"] = int(resp[0])
    output["fromTime"] = int(fromTime)
    output["toTime"] = int(toTime)
    #units are in Gwei
    return '{ "error": false, "message":' + str(output) + '}'

if __name__ == "__main__":
    app.run(port=8880)
