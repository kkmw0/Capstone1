#-*- coding: utf-8 -*-
import pymysql

bus_db = pymysql.connect(
    user = 'admin',
    passwd = 'kkmw0915!!',
    host = 'busdb.cukujwnz1i1a.us-west-2.rds.amazonaws.com',
    db = 'busDB',
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

def search_Station(stationName):
    result = []
    ch = u'정'
    cursor = bus_db.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT stationName FROM station WHERE UPDOWN LIKE '%"+ch+"%' and stationName LIKE '"+stationName+"%';"
    cursor.execute(sql)
    tmp = cursor.fetchall()

    for i in range(len(tmp)):
        result.append(tmp[i]['stationName'])

    return result

def search_Bus(busNum):
    result = []
    cursor = bus_db.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT busNum FROM bus WHERE busNum LIKE '"+busNum+"%';"
    cursor.execute(sql)
    tmp = cursor.fetchall()

    for i in range(len(tmp)):
        result.append(tmp[i]['busNum'])

    return result
