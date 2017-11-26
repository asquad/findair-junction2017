import csv
import requests
from random import shuffle
from operator import itemgetter
from datetime import datetime
import random

def getAirportsDict(mode='EUR'):
    finnairflights = list()
    with open('data/Flight_Schedule.csv', 'r') as csvfile:
        finnreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in finnreader:
            finnairflights.append(row)
    dep = 'HEL'
    arr = 'GOT'
    airportsCodes = list()
    #16, 17
    for i in finnairflights:
        # print (i[16])
        # if (i[16]==dep and i[17]==arr):
        # print (i[16],i[17])
        # if i[16] not in airportsCodes and len(i[16])==3:
        #     airportsCodes.append(i[16])
        if i[17] not in airportsCodes and len(i[17])==3:
            airportsCodes.append(i[17])
    airportsCities = dict()
    euroCountryCodes = ['IS', 'LI', 'CH', 'NO', 'BE', 'BG', 'CZ', 'DK', 'DE', 'IE', 'EE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'UK']
    with open('data/IATA.csv', 'r') as csvfile:
        airportsreader = csv.reader(csvfile, delimiter='^')
        # i=0
        for row in airportsreader:
            # if (len(row[1])==3):
            # print (row[0])
            for j in airportsCodes:
                if (mode=='ALL'):
                    if (row[0]==j):
                        airportsCities[j] = row[1]
                elif (mode=='EUR' and row[3] in euroCountryCodes):
                    if (row[0]==j):
                        airportsCities[j] = row[1]
            # i+=1
    return (airportsCities)


def findFlights(airportsCities, arrDate, depDate,priceLimit, limit ):
    # https://instantsearch-junction.ecom.finnair.com/api/instantsearch/pricesforperiod?departureLocationCode=HEL&destinationLocationCode=STO&startDate=2017-12-12&numberOfDays=1
    result = list()
    counter = 0
    foundedCount = 0
    for i in (airportsCities.items()):
        # print (i)
        
        depCity = 'HEL'


        date_format = "%Y-%m-%d"
        a = datetime.strptime(arrDate, date_format)
        b = datetime.strptime(depDate, date_format)
        delta = b - a
        # print ()


        curRes = dict()
        r = requests.get('https://instantsearch-junction.ecom.finnair.com/api/instantsearch/pricesforperiod?departureLocationCode='+depCity+'&destinationLocationCode=' + i[0] + '&startDate=' + arrDate + '&numberOfDays='+str(delta.days))
        responseArr = r.json()
        if (responseArr.get('errorCode') or responseArr.get('level')):
            # print ('EEEEEEEEEERRRRRRRROOOOOOORRRRRRR')
            continue
        # print ('~~~~~' + str(responseArr))
        destCity = responseArr['dest']

        priceArr = None
        priceId = 0
        while (priceArr is None and priceId<len(responseArr['prices'])):
            priceArr = responseArr['prices'][priceId]['price']
            priceId+=1
            # print (priceId)

        if (priceArr is None or priceArr>priceLimit):
            # print ('SKIP')
            continue

        # r = requests.get('https://instantsearch-junction.ecom.finnair.com/api/instantsearch/pricesforperiod?departureLocationCode='+destCity+'&destinationLocationCode='+depCity+'&startDate=' + depDate + '&numberOfDays=1')
        # responseDep = r.json()
        # if (responseDep.get('errorCode')):
        #     continue
        # print ('~~~' + str(responseDep))
        # priceDep = responseDep['prices'][0]['price']

        curRes['depCity'] = airportsCities[depCity]
        curRes['destCity'] = airportsCities[destCity]
        curRes['price'] = priceArr
        curRes['dateArrive'] = arrDate
        curRes['dateDeparture'] = depDate

        result.append(curRes)
        foundedCount+=1
        print (str(foundedCount) + ' founded!')

        counter+=1
        if (counter>limit-1):
            break


        
    # print  (result)
    result = sorted(result, key=itemgetter('price')) 
    return result




def findCoolCity(arrDate, depDate, priceLimit):
    cities = getAirportsDict()
    res = findFlights(cities, arrDate, depDate, priceLimit, 3)
    return res[random.randint(0,len(res)-1)]

#print (findCoolCity('2017-12-05', '2017-12-12', 600))
