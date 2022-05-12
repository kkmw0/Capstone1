import requests, xmltodict, json

key = "T4WmEeuAgyLD6LuyLjyHemjnQaJMLRhciWrVRoaBYwRkP6S64W4ZJuhgJt42DjWFQF%2ByYnzwE8Xl7eiZ2kyRlA%3D%3D"

def bus_stationList(routeID):
    stationList_url = "http://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList?serviceKey={0}&routeId={1}".format(key, routeID)

    content = requests.get(stationList_url).content
    dict = xmltodict.parse(content)

    jsonString = json.dumps(dict['response']['msgBody']['busRouteStationList'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    return jsonObj

def bus_predictTime(stationID):
    stationList_url = "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList?serviceKey={0}&stationId={1}".format(key, stationID)

    content = requests.get(stationList_url).content
    dict = xmltodict.parse(content)

    jsonString = json.dumps(dict['response']['msgBody']['busArrivalList'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    return jsonObj
