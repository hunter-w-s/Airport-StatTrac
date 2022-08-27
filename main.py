from datetime import datetime, timedelta
import sys, time, requests, json

sys.path = ['/home/hwstingel/SeniorProject/Airport-StatTrac', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/home/hwstingel/.local/lib/python3.9/site-packages', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']

querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}
headers = {"X-RapidAPI-Key": "KEY","X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}

#Define Storage Lists
airport = 'KCLT'

startTimeList = ['00','06','12','18']
toTimeList = ['06','12','18','00']

while(True):
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    urlList = []
    for x in range(4):
        if x == 3:
            urlList.append("https://aerodatabox.p.rapidapi.com/flights/airports/icao/{}/{}T{}:00/{}T{}:00".format(airport,yesterday,startTimeList[x],today,toTimeList[x]))
            continue
        urlList.append("https://aerodatabox.p.rapidapi.com/flights/airports/icao/{}/{}T{}:00/{}T{}:00".format(airport,yesterday,startTimeList[x],yesterday,toTimeList[x]))
    
    fullListDep = []
    fullListArr = []
    
    for each in urlList:
        response = requests.request("GET", each, headers=headers, params=querystring)
        fullListDep = fullListDep + response.json()['departures']
        fullListArr = fullListArr + response.json()['arrivals']
    
    print(len(fullListDep))
    print(len(fullListArr))
    
    while True:
        continue
    
    time.sleep(60)
        
        
        