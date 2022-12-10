from datetime import datetime, timedelta
import sys, requests, json, config
import pandas as pd

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
    day = (datetime.now() - timedelta(config.daysAgo-1)).strftime('%d')
    month = (datetime.now() - timedelta(config.daysAgo-1)).strftime('%m')
    year = (datetime.now() - timedelta(config.daysAgo-1)).strftime('%Y')
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow = (datetime.now() - timedelta(config.daysAgo-1)).weekday()
    dow = days[dow]
    yesterday = (datetime.now() - timedelta(config.daysAgo)).strftime('%Y-%m-%d')

    fullListDep = []
    fullListArr = []
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

    df = pd.read_csv('depData.csv', sep=',',converters={'day':str, 'month':str, 'year':str, 'dow':str,'hour':str, 'min':str, 'depICAO':str, 'canc':bool, 'craftType':str})
    df.drop(columns = df.columns[0], axis = 1, inplace= True)
    for each in fullListDep:
        try:
            if "Boeing" in each["aircraft"]["model"]:
                aircraft = "Boeing"
            elif "Airbus" in each["aircraft"]["model"]:
                aircraft = "Airbus"
            elif "Embraer" in each["aircraft"]["model"]:
                aircraft = "Embraer"
            elif "Canadair"  in each["aircraft"]["model"] or "Bombradier" in each["aircraft"]["model"] or "CRJ" in each["aircraft"]["model"]:
                aircraft = "Canadair Regional"
            else:
                aircraft = "Other"
            df.loc[len(df.index)] = [day, month, year, dow,each['departure']['scheduledTimeLocal'][11:13],each['departure']['scheduledTimeLocal'][14:16],each['arrival']['airport']['icao'],aircraft,each["airline"]["name"]]

        except Exception as e:
            print(e)
            continue

    print(df.head())
    print(df.shape)
    
    df.to_csv('depData.csv', sep=',')

    df = pd.read_csv('arrData.csv', sep=',',converters={'day':str, 'month':str, 'year':str, 'dow':str,'hour':str, 'min':str, 'depICAO':str, 'canc':bool, 'craftType':str})
    df.drop(columns = df.columns[0], axis = 1, inplace= True)
    for each in fullListArr:
        
        try:
            if "Boeing" in each["aircraft"]["model"]:
                aircraft = "Boeing"
            elif "Airbus" in each["aircraft"]["model"]:
                aircraft = "Airbus"
            elif "Embraer" in each["aircraft"]["model"]:
                aircraft = "Embraer"
            elif "Canadair"  in each["aircraft"]["model"] or "Bombradier" in each["aircraft"]["model"] or "CRJ" in each["aircraft"]["model"]:
                aircraft = "Canadair Regional"
            else:
                aircraft = "Other"
            df.loc[len(df.index)] = [day, month, year, dow,each['arrival']['scheduledTimeLocal'][11:13],each['arrival']['scheduledTimeLocal'][14:16],each['departure']['airport']['icao'],aircraft,each["airline"]["name"]]

        except Exception as e:
            print(e)
            continue

    df.to_csv('arrData.csv', sep=',')


    
    print(df.head())
    print(df.shape)
    
    


if __name__ == "__main__":
    logFlights()
