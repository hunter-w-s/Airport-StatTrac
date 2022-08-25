from datetime import datetime
from FlightRadar24.api import FlightRadar24API
import sys, time


sys.path = ['/home/hwstingel/SeniorProject/Airport-StatTrac', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/home/hwstingel/.local/lib/python3.9/site-packages', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']

fr = FlightRadar24API()

flights = fr.get_flights()

#Define Storage Lists
trackedIncoming = []
lostIncoming = []
trackedOutgoing = []
newOutgoing = []

knownIncoming = []
knownOutgoing = []

outboundCt = 0
inboundCt = 0

takeoffCt = 0
landingCt = 0

while(True):

    flights = fr.get_flights()
    for each in flights:
        if each.destination_airport_iata == 'CLT' and int(each.altitude) >= 1000:
            trackedIncoming.append(each)
            
        if each.origin_airport_iata == 'CLT' and int(each.altitude) >= 1000:
            trackedOutgoing.append(each) 
            
           
    #Checks if tracked flight is a new departure
    for each in trackedOutgoing:
        if each in trackedOutgoing:
            continue
        else:
            newOutgoing.append(each)
            
    takeoffCt = len(newOutgoing)

    for each in newOutgoing:
        knownOutgoing.append(each)

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
        if each[1] => 5:
            landingCt += 1
        
        
        
        
