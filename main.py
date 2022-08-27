from datetime import datetime, timedelta
import sys, time, requests, json, schedule

sys.path = ['/home/hwstingel/SeniorProject/Airport-StatTrac', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/home/hwstingel/.local/lib/python3.9/site-packages', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']

querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}
headers = {"X-RapidAPI-Key": "KEY","X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}

#Define Storage Lists
airport = 'KCLT'

startTimeList = ['00','06','12','18']
toTimeList = ['06','12','18','00']

def logFlights():
    today = (datetime.now() - timedelta(3)).strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(4)).strftime('%Y-%m-%d')
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
    
    cancDep = 0
    cancArr = 0
    
    aircraftListDep = []
    aircraftListArr = []
    airlineListDep = {}
    airlineListArr = {}
    
    for each in fullListDep:
        if "Canceled" in each['status']:
            cancArr += 1
        if "aircraft" in each.keys():
            if "model" in each["aircraft"].keys():
                if each["aircraft"]["model"] not in aircraftListDep:
                    aircraftListDep.append(each["aircraft"]["model"])
        if "airline" in each.keys():
            if each["airline"]["name"] not in airlineListDep.keys():
                airlineListDep[each["airline"]["name"]] = 1
            else:
                airlineListDep[each["airline"]["name"]] += 1
        
    for each in fullListArr:
        if "Canceled" in each['status']:
            cancDep += 1      
        if "aircraft" in each.keys():
            if "model" in each["aircraft"].keys():
                if each["aircraft"]["model"] not in aircraftListArr:
                    aircraftListArr.append(each["aircraft"]["model"])
        if "airline" in each.keys():
            if each["airline"]["name"] not in airlineListArr.keys():
                airlineListArr[each["airline"]["name"]] = 1
            else:
                airlineListArr[each["airline"]["name"]] += 1
    
    
    print(aircraftListDep)
    print(aircraftListArr)
    
    print(airlineListDep)
    print(airlineListArr)
    
    print(cancDep)
    print(cancArr)
    
schedule.every().day.at("8:00").do(logFlights)

while True:
    schedule.run_pending()
    time.sleep(60)
        
        
        