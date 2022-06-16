#-*- coding: utf-8 -*-

from flask import Flask, jsonify
import json
import db_connect
import getbus

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/getStationStop/<busNum>', methods=['GET', 'POST'])
def extract_StationList(busNum):
    result = db_connect.getRouteID(busNum)
    busInfo = getbus.bus_stationList(result)

    bus = []
    for i in range(len(busInfo)):
        if busInfo[i]['turnYn'] == 'Y':
            bus.append({'stationName' : busInfo[i]['stationName'] + u"(회차)"})
        else:
            bus.append({'stationName' : busInfo[i]['stationName']})
    return jsonify(bus)

@app.route('/getPredictTime/<StationName>', methods=['GET', 'POST'])
def extract_PredictTime(StationName):
    result = db_connect.getStationID(StationName)
    busInfo = getbus.bus_predictTime(result)

    predictTime = []
    stationID = []
    result_PredictTime = []
    result_busNum = []

    getPredict = []
    for i in range(len(busInfo)):
        #predictTime.append(busInfo[i]['predictTime1'] + "min")
        stationID.append(busInfo[i]['routeId'])

    busNum = db_connect.routeID_to_busNum(stationID)
    for i in range(len(busNum)):
        getPredict.append({'busNum' : busNum[i] + u'번', 'predictTime' : busInfo[i]['predictTime1'] + u'분'})
    #getPredict = {'PredictTime' : predictTime, 'busNum' : tmp}
    return jsonify(getPredict)

#    for i in range(len(busInfo)):
#        result_PredictTime.append(predictTime[i])
#        result_busNum.append(tmp[i])

@app.route('/getStationList/<StationName>', methods=['GET', 'POST'])
def extract_stationList(StationName):
    result = db_connect.search_Station(StationName)
    return jsonify(result)

@app.route('/getBusList/<busNum>', methods=['GET', 'POST'])
def extract_busList(busNum):
    result = db_connect.search_Bus(busNum)
    #result.sort()
    #busList = dict(zip(range(1, len(result) + 1), result))
    return jsonify(result)

@app.route('/getBusCurrentPos/<busNum>/<plateNo>', methods=['GET', 'POST'])
def extract_currentPos(busNum, plateNo):
    result = db_connect.bus_destination(busNum, plateNo)
    return jsonify(result)

if  __name__ == '__main__':
    app.run(host = '172.31.23.80', port = 12345, debug = True)
