from datetime import datetime, timedelta
import sys, requests, json, config

#For use on Rasp Pi for execution in terminal, not necessary in IDE
#sys.path = ['/home/hwstingel/SeniorProject/Airport-StatTrac', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/home/hwstingel/.local/lib/python3.9/site-packages', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']

querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}
headers = {"X-RapidAPI-Key": config.apiKey,"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}


#Primary Use - Round minute input down to the nearest 15 for cataloging
def round15(mins):
    if mins == "00":
        return "00"
    elif int(mins) <= 14:
        return "00"
    elif int(mins) <= 29:
        return "15"
    elif int(mins) <= 44:
        return "30"
    else:
        return "45"
        

#Main Execution function
def logFlights():
    #Define Constants
    airport = config.airportICAO
    startTimeList = ['00','08','16']
    toTimeList = ['08','16','00']
    today = (datetime.now() - timedelta(config.daysAgo-1)).strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(config.daysAgo)).strftime('%Y-%m-%d')

    #Define storage Variable for Data
    cancDep = 0
    cancArr = 0
    depSched = 0
    arrSched = 0
    fullListDep = []
    fullListArr = []
    aircraftListDep = {"Boeing":0,"Airbus":0,"Canadair Regional":0,"Embraer":0,"Other":0}
    aircraftListArr = aircraftListDep
    airlineListDep = {}
    airlineListArr = {}
    destination = {}
    origin = {}
    timeInfoDep = {"dataDate":yesterday,"hours":{"00":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "01":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "02":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "03":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "04":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "05":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "06":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "07":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "08":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "09":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "10":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "11":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "12":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "13":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "14":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "15":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "16":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "17":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "18":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "19":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "20":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "21":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "22":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 "23":{"00":{"scheduled":0,"numCanc":0},"15":{"scheduled":0,"numCanc":0},"30":{"scheduled":0,"numCanc":0},"45":{"scheduled":0,"numCanc":0}},
                                                 }}
    timeInfoArr = timeInfoDep

    #Generates URLs and fetches data
    for x in range(len(startTimeList)):
        if x == len(startTimeList)-1:
            response = requests.request("GET", ("https://aerodatabox.p.rapidapi.com/flights/airports/icao/{}/{}T{}:00/{}T{}:00".format(airport,yesterday,startTimeList[x],today,toTimeList[x])), headers=headers, params=querystring)
            fullListDep = fullListDep + response.json()['departures']
            fullListArr = fullListArr + response.json()['arrivals']
            continue
        response = requests.request("GET", ("https://aerodatabox.p.rapidapi.com/flights/airports/icao/{}/{}T{}:00/{}T{}:00".format(airport,yesterday,startTimeList[x],yesterday,toTimeList[x])), headers=headers, params=querystring)
        fullListDep = fullListDep + response.json()['departures']
        fullListArr = fullListArr + response.json()['arrivals']    

    #Sorts and Cleans Data and Transoforms into usable dictionaries
    for each in fullListDep:

        if "departure" in each.keys():
            schedHour = each["departure"]["scheduledTimeLocal"][11:13]
            schedMin = each["departure"]["scheduledTimeLocal"][14:16]

            timeInfoDep["hours"][schedHour][round15(schedMin)]["scheduled"] += 1
            depSched += 1
        else:continue

        if "arrival" in each.keys():
            if "airport" in each["arrival"].keys():
                if "iata" in each["arrival"]["airport"].keys() and "name" in each["arrival"]["airport"].keys():
                    if "{} / {}".format(each["arrival"]["airport"]["iata"],each["arrival"]["airport"]["name"]) in destination.keys():
                        destination["{} / {}".format(each["arrival"]["airport"]["iata"],each["arrival"]["airport"]["name"])] += 1
                    else:
                        destination["{} / {}".format(each["arrival"]["airport"]["iata"],each["arrival"]["airport"]["name"])] = 1
                    

        
        if "airline" in each.keys():
            if each["airline"]["name"] == 'Unknown/Private owner':
                continue
            if each["airline"]["name"] not in airlineListDep.keys():
                airlineListDep[each["airline"]["name"]] = 1
            else:
                airlineListDep[each["airline"]["name"]] += 1
        if "Canceled" in each['status']:
            cancDep += 1
            timeInfoDep["hours"][schedHour][round15(schedMin)]["numCanc"] += 1

        if "aircraft" in each.keys():
            if "model" in each["aircraft"].keys():
                if "Boeing" in each["aircraft"]["model"]:
                    aircraftListDep["Boeing"] += 1
                elif "Airbus" in each["aircraft"]["model"]:
                    aircraftListDep["Airbus"] += 1
                elif "Embraer" in each["aircraft"]["model"]:
                    aircraftListDep["Embraer"] += 1
                elif "Canadair"  in each["aircraft"]["model"] or "Bombradier" in each["aircraft"]["model"] or "CRJ" in each["aircraft"]["model"]:
                    aircraftListDep["Canadair Regional"] += 1
                else:
                    aircraftListDep["Other"] += 1
        
    for each in fullListArr:

        if "arrival" in each.keys():
            schedHour = each["arrival"]["scheduledTimeLocal"][11:13]
            schedMin = each["arrival"]["scheduledTimeLocal"][14:16]

            timeInfoArr["hours"][schedHour][round15(schedMin)]["scheduled"] += 1
            arrSched += 1
        else:continue

        if "departure" in each.keys():
            if "airport" in each["departure"].keys():
                if "iata" in each["departure"]["airport"].keys() and "name" in each["departure"]["airport"].keys():
                    if each["departure"]["airport"]["name"] in origin.keys():
                        origin["{} / {}".format(each["departure"]["airport"]["iata"],each["departure"]["airport"]["name"])] += 1
                    else:
                        origin["{} / {}".format(each["departure"]["airport"]["iata"],each["departure"]["airport"]["name"])] = 1
        
        if "airline" in each.keys():
            if each["airline"]["name"] == 'Unknown/Private owner':
                continue
            if each["airline"]["name"] not in airlineListArr.keys():
                airlineListArr[each["airline"]["name"]] = 1
            else:
                airlineListArr[each["airline"]["name"]] += 1
                
        if "Canceled" in each['status']:
            cancArr += 1
            timeInfoArr["hours"][schedHour][round15(schedMin)]["numCanc"] += 1
            
        if "aircraft" in each.keys():
            if "model" in each["aircraft"].keys():
                if "Boeing" in each["aircraft"]["model"]:
                    aircraftListArr["Boeing"] += 1
                elif "Airbus" in each["aircraft"]["model"]:
                    aircraftListArr["Airbus"] += 1
                elif "Embraer" in each["aircraft"]["model"]:
                    aircraftListArr["Embraer"] += 1
                elif "Canadair"  in each["aircraft"]["model"] or "Bombradier" in each["aircraft"]["model"] or "CRJ" in each["aircraft"]["model"]:
                    aircraftListArr["Canadair Regional"] += 1
                else:
                    aircraftListArr["Other"] += 1

    #Saves each collection of data as a dictionry then saves as a respective JSON
    dayDepInfo = {"totals":{"scheduledFlights":depSched,"numCanceled": cancDep,"airlineCounts":airlineListDep,"aircraftCounts":aircraftListDep, "destinationCounts":destination},"timeInfo":timeInfoDep}
    dayArrInfo = {"totals":{"scheduledFlights":arrSched,"numCanceled": cancArr,"airlineCounts":airlineListArr,"aircraftCounts":aircraftListArr, "originCounts":origin},"timeInfo":timeInfoArr}

    with open('deps.json', 'w') as fp:
        json.dump(dayDepInfo, fp, sort_keys=False, indent=4)
    with open('arrs.json', 'w') as fp:
        json.dump(dayArrInfo, fp, sort_keys=False, indent=4)
    


if __name__ == "__main__":
    logFlights()
