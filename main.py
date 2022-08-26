from datetime import datetime
from FlightRadar24.api import FlightRadar24API
import sys, time, requests, json


sys.path = ['/home/hwstingel/SeniorProject/Airport-StatTrac', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/home/hwstingel/.local/lib/python3.9/site-packages', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']


params = {
    'api_key':'db3e29aa-6280-433c-b3e1-49a4db3ff07d',
    'dep_icao': 'KCLT'
    }

method = 'flights'
api_base = 'http://airlabs.co/api/v9/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()

print(json.dumps(api_response, indent=4, sort_keys=True))

while True:
    continue


fr = FlightRadar24API()

flights = fr.get_flights()

#Define Storage Lists
trackedIncoming = []
lostIncoming = []
lostOutgoing = []
trackedOutgoing = []
newOutgoing = []

knownIncoming = []
knownOutgoing = []
knownOutgoingCounter = []

outboundCt = 0
inboundCt = 0

takeoffCt = 0
landingCt = 0

while(True):

    flights = fr.get_flights(bounds = '36 34 -82 -80')
    for each in flights:
        if each.destination_airport_iata == 'CLT' and int(each.altitude) >= 1000:
            trackedIncoming.append(each.id)
            
        if each.origin_airport_iata == 'CLT' and int(each.altitude) >= 1000:
            trackedOutgoing.append(each.id) 
    
    print(trackedOutgoing)
    print(trackedIncoming)
           
    #Checks if tracked flight is a new departure
    for each in trackedOutgoing:
        if each in knownOutgoing:
            continue
        else:
            newOutgoing.append(each)
            
    takeoffCt = len(newOutgoing)
    
    for each in knownOutgoingCounter:
        if each[0] in newOutgoing:
            newOutgoing.remove(each)
    
    
    for each in newOutgoing:
        knownOutgoing.append(each)
        knownOutgoingCounter.append([each,0])
        
    for each in knownOutgoingCounter:
        if each[0] not in knownOutgoing:
            each[1] += 1
        if each[1] >= 5:
            knownOutgoingCounter.remove(each)

    #Checks if an aircraft lost contact indicating landing
        
        
    for each in lostIncoming:
        if each[0] in trackedIncoming:
            lostIncoming.remove(each)
        else:
            each[1] += 1
        

    for each in knownIncoming:
        if each not in trackedIncoming:
            lostIncoming.append([each,0])
            
    for each in lostIncoming:
        if each[1] >= 5:
            landingCt += 1
            lostIncoming.remove(each)
            
            
    print(newOutgoing)
    print(lostIncoming)
    
    newOutgoing.clear()
    
    time.sleep(180)
        
        
        
        
