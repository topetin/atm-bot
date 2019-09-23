import requests
import math
import json
from pprint import pprint
import copy

def getAtmData(atmType, latitude, longitude, distance, maxAtmsToList):
    payload = {"resource_id":"28.1","q":"","filters":{"localidad":"CABA","red":atmType},"limit":1000,"offset":0}
    headers = {'Content-Type': 'application/json'}
    r = requests.post("https://data.buenosaires.gob.ar/api/3/action/datastore_search", data=json.dumps(payload), headers=headers, verify=True)
    results = json.loads(r.text)
    atmResults = results['result']['records']
    
    allNearestAtms = getNearestAtms(atmResults, latitude, longitude, distance)
    for atm in allNearestAtms:
        lat = atm.get('lat')
        lon = atm.get('long')
        dist = calcDistance(latitude, longitude, lat, lon)
        atm['distance_to_user'] = dist

    allNearestAtmsSorted = sorted(allNearestAtms, key = lambda i: i['distance_to_user'])
    nearestAtms = allNearestAtmsSorted[:maxAtmsToList]
    return nearestAtms

def getNearestAtms(results, latitude, longitude, distance):
    userDistance = calculateDistance(latitude, longitude, distance)
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

def calculateDistance(latitude, longitude, distance):
    kmInLongitudeDegree = 111.320 * math.cos( latitude / 180.0 * math.pi)
    deltaLat = distance / 111.1
    deltaLon = distance / kmInLongitudeDegree
    minLat = latitude - deltaLat
    maxLat = latitude + deltaLat
    minLon = longitude - deltaLon
    maxLon = longitude + deltaLon
    return {'minLat': minLat, 'maxLat': maxLat, 'minLon': minLon, 'maxLon': maxLon}

def calcDistance(latOrigin, lonOrigin, latDest, lonDest):
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