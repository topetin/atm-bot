import copy

def formatPhotoUrl(userLat, userLon, atms):
    base = "https://maps.googleapis.com/maps/api/staticmap?"
    zoom = "&zoom=15"
    size = "&size=400x400"
    maptype = "&maptype=roadmap"
    userMarker = f"&markers=color:blue%7C{userLat},{userLon}"
    atmMarkers = []
    key = "&key=" #Google API Key

    for atm in atms:
        atmLat = atm.get('lat')
        atmLon = atm.get('long')
        atmMarker = f"&markers=color:red%7Clabel:{atms.index(atm)+1}%7C{atmLat},{atmLon}"
        atmMarkers.append(atmMarker)

    finalUrl = base + zoom + size + maptype + userMarker
    
    for marker in atmMarkers:
        finalUrl += marker

    finalUrl += key 
    return finalUrl

def formatAtmName(atm):
    atmType = copy.copy(atm)
    atmTypeFormatted = atmType[1:].upper()
    return atmTypeFormatted