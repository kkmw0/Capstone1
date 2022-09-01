#-*- coding: utf-8 -*-
import pymysql
import requests, xmltodict, json
import urllib3
import time

urllib3.disable_warnings()
key = "Your Private Key"

bus_db = pymysql.connect(
    user = 'Your Id',
    passwd = 'Your Password',
    host = 'Your DB endpoint',
    db = 'DB Name',
    charset='utf8'
)

def getRouteID(busNum):
    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT routeID FROM bus WHERE busNum = %s;"
    cursor.execute(sql, (busNum))
    result = cursor.fetchone()
    return result['routeID']

def getStationID(stationName):
    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT busStationID FROM station WHERE stationName = %s;"
    cursor.execute(sql, (stationName))
    result = cursor.fetchone()
    return result['busStationID']

def routeID_to_busNum(routeID):
    result = []
    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT busNum FROM bus WHERE routeID = %s;"
    for i in range(len(routeID)):
        cursor.execute(sql, (routeID[i]))
        tmp = cursor.fetchone()
        if tmp is not None:
            result.append(tmp['busNum'])

    return result

def getStationName(stationID):
    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT stationName, direction FROM station WHERE busStationID = %s;"
    cursor.execute(sql, (stationID))
    result = cursor.fetchone()

    return result['stationName'] + "(" + result['direction'] + u" 방면" + ")"

def search_Station(stationName):
    result = []
    i = 0
    ch = u'정'
    cursor = bus_db.cursor()

    sql = "SELECT DISTINCT stationName, direction FROM station WHERE stationName LIKE '"+stationName+"%' ORDER BY stationName;"
    cursor.execute(sql)
    for row in cursor:
        result.append({'stationName' : row[0], 'direction' : row[1]})
        i += 1

    return result

def search_Bus(busNum):
    result = []
    i = 0
    cursor = bus_db.cursor()

    sql = "SELECT busNum, startStation, endStation FROM bus WHERE busNum LIKE '"+busNum+"%' ORDER BY busNum;"
    cursor.execute(sql)
    for row in cursor:
        result.append({'busNum' : row[0], 'startStation' : row[1], 'endStation' : row[2]})
        i += 1

#    for i in range(len(tmp)):
#        result.append(tmp[i]['busNum'])

    return result

def bus_destination(busNum, plateNo):
    stationID = ""

    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT routeID FROM bus WHERE busNum = %s;"
    cursor.execute(sql, (busNum))
    result = cursor.fetchone()
    routeID = result['routeID']

    buslocation_url = "https://apis.data.go.kr/6410000/buslocationservice/getBusLocationList?serviceKey={0}&routeId={1}".format(key, routeID)
    content = requests.get(buslocation_url, verify=False).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['response']['msgBody']['busLocationList'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    for i in range(len(jsonObj)):
        if jsonObj[i]['plateNo'] == plateNo:
            stationID = jsonObj[i]['stationId']
            break

    current_location = getStationName(stationID)
    return current_location
