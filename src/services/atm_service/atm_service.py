import requests
import math
import json
import copy
from data_handler.data_handler import hasAvailableWithdraw


def findAtms(atmType, latitude, longitude):
    results = getAtmData(atmType, latitude, longitude)
    maxDistance = 0.5
    maxAtmsToList = 3
    allNearestAtms = filterNearestAtms(results, latitude, longitude, maxDistance)
    withCashAtms = []
    for atm in allNearestAtms:
        if hasAvailableWithdraw(atm.get('red'), atm.get('id')):
            lat = atm.get('lat')
            lon = atm.get('long')
            dist = calculateDistanceToAtm(latitude, longitude, lat, lon)
            atm['distance_to_user'] = dist
            withCashAtms.append(atm)
    withCashAtmsSorted = sorted(withCashAtms, key = lambda i: i['distance_to_user'])
    bestNearestAtms = withCashAtmsSorted[:maxAtmsToList]
    return bestNearestAtms


def getAtmData(atmType, latitude, longitude):
    payload = {"resource_id":"28.1","q":"","filters":{"localidad":"CABA","red":atmType},"limit":1000,"offset":0}
    headers = {'Content-Type': 'application/json'}
    url = "https://data.buenosaires.gob.ar/api/3/action/datastore_search"
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=True)
    results = json.loads(response.text)
    atmResults = results['result']['records']
    return atmResults


def filterNearestAtms(results, latitude, longitude, maxDistance):
    userDistance = calculateMaxAndMinDistance(latitude, longitude, maxDistance)
    nearAtms = []
    for atmData in results:
        atmLat = atmData.get('lat')
        atmLon = atmData.get('long')
        if isNearAtm(atmLat, atmLon, userDistance):
            nearAtms.append(copy.copy(atmData))
    return nearAtms


def isNearAtm(atmLat, atmLon, userDistance):
    minLat = userDistance.get('minLat')
    maxLat = userDistance.get('maxLat')
    minLon = userDistance.get('minLon')
    maxLon = userDistance.get('maxLon')
    if  minLat <= atmLat <= maxLat and minLon <= atmLon <= maxLon:
        return True    
    return False


def calculateMaxAndMinDistance(latitude, longitude, maxDistance):
    kmInLongitudeDegree = 111.320 * math.cos( latitude / 180.0 * math.pi)
    deltaLat = maxDistance / 111.1
    deltaLon = maxDistance / kmInLongitudeDegree
    minLat = latitude - deltaLat
    maxLat = latitude + deltaLat
    minLon = longitude - deltaLon
    maxLon = longitude + deltaLon
    return {'minLat': minLat, 'maxLat': maxLat, 'minLon': minLon, 'maxLon': maxLon}


def calculateDistanceToAtm(latOrigin, lonOrigin, latDest, lonDest):
    lat1= latOrigin
    lon1 = lonOrigin
    lat2 = latDest
    lon2 = lonDest
    radius = 6371

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d