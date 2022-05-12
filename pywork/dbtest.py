from flask import Flask, jsonify
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
        bus.append(busInfo[i]['stationName'])
    return jsonify(bus)

@app.route('/getPredictTime/<StationName>', methods=['GET', 'POST'])
def extract_PredictTime(StationName):
    result = db_connect.getStationID(StationName)
    busInfo = getbus.bus_predictTime(result)

    predictTime = []
    stationID = []
    result = []

    for i in range(len(busInfo)):
        predictTime.append(busInfo[i]['predictTime1'] + "min")
        stationID.append(busInfo[i]['routeId'])

    tmp = db_connect.routeID_to_busNum(stationID)
    for i in range(len(busInfo)):
        result.append([predictTime[i], tmp[i]])

    return jsonify(result)

@app.route('/getStationList/<StationName>', methods=['GET', 'POST'])
def extract_stationList(StationName):
    result = db_connect.search_Station(StationName)
    return jsonify(result)

@app.route('/getBusList/<busNum>', methods=['GET', 'POST'])
def extract_busList(busNum):
    result = db_connect.search_Bus(busNum)
    return jsonify(result)

if  __name__ == '__main__':
    app.run(host = '172.31.23.80', port = 12345, debug = True)
