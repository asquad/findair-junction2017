
# -*- coding: utf-8 -*-

import foursquare
import json
import random

# Construct the client object
# client = foursquare.Foursquare(client_id='UM3WI1J2AG25RFS3RPL41CYBU3YPDDUNF5SZ50ANTUSJWXTD', client_secret='1MRI5YLQI3EJ2HBOF3LI2AU20DRQ2ERTP4X5TTWY2EHAMVYB', redirect_uri='https://google.com')

client = foursquare.Foursquare(client_id='W2SZVTQVI33MNHPMQGG2S5XXFAQ5Y0KDSHL2OQJBCLIIFSON', client_secret='SWN3WP44OY32QPR11P5TMBHRFYXA5VI25OPKPQGP2Y0UO43X', redirect_uri='https://google.com')
# results = client.venues.search(params={'query': 'burger', 'll': '60.168544,24.941708', 'limit': '50', 'radius':'15000', 'intent':'browse'})

# 'll': '60.168544,24.941708'

from operator import itemgetter


def findPlaces(location, query):
    places = list()
    results = client.venues.explore(params={'near':location, 'limit': '5', 'radius':'10000',  'query':query, 'openNow':'0', 'sortByDistance':'0'})

    num = 0
    for i in results["groups"][0]["items"]:

        curPlace = dict()

        num+=1
        ven = i["venue"]
        venid = ven["id"]
        ven = client.venues(VENUE_ID=venid)["venue"]


        if (ven.get('rating')):
            rating = float(ven['rating'])
        else:
            rating = 0.0

        curPlace['rating'] = rating
        curPlace['name'] = ven['name']

        isSecondAdr = False
        biggestRating = 0.0
        biggestRatingId = 0
        curId = 0
        # print (places)
        for k in places:
            if (k['name']==curPlace['name']):
                isSecondAdr = True
                if (k['rating']>biggestRating):
                    biggestRating = k['rating']
                biggestRatingId=curId
            curId+=1
                

        if (isSecondAdr):
            if (rating>biggestRating):
                places[biggestRatingId]["rating"] = rating
            # print (biggestRating, rating)
            continue

        # tags, phrases and descr
        tags = ven['tags']
        tmpstr = str(num) + ' ' + str(rating) + ' ' + ven['name'] + ' =>'
        staff = ''
        for j in tags:
            tmpstr += ' ' + j
            staff += j + ' '
        if (ven.get('phrases')):
            for j in ven['phrases']:
                tmpstr += ' ' + j['phrase']
                staff += j['phrase'] + ' '

        if (ven.get('description')):
            staff += ven['description']
	
	tip = ven['tips']['groups'][0]['items'][random.randint(0,len(ven['tips']['groups'][0]['items'])-1)]['text']
#        if (len(ven['tips']['groups'][0]['items'])>0):
#            for i in ven['tips']['groups'][0]['items']:
#                #print('~~~~' + i['text'])
#                staff+=' '+i['text']

        photourl = None
        if (len(ven['photos']['groups'])>0):
            photourl = ven['photos']['groups'][0]['items'][0]['prefix']+'2000x1000'+ven['photos']['groups'][0]['items'][0]['suffix']
        # print (photourl)

        try:
            curPlace['category'] = ven["categories"][0]["pluralName"]
        except:
            curPlace['category'] = "Unknown"
        curPlace['image'] = photourl
        curPlace['stuff'] = staff 
        curPlace['tip'] =tip 

        #price
        price = 0
        if (ven.get('price')):
            price = ven['price']['tier']
        else:
            price = random.randint(1,2)
            # print(ven['price']['tier'])

        if (price==1):
            price = random.randint(3,10)
        elif (price==2):
            price = random.randint(11,20)
        elif (price==3):
            price = random.randint(21,35)
        elif (price==4):
            price = random.randint(36,55)


        curPlace['price'] = price

        if (staff!=''):
            places.append(curPlace)

    return sorted(places, key=itemgetter('rating'), reverse=True)
        # print ( tmpstr )


#res = findPlaces('Paris', 'food museum hospital')

#from operator import itemgetter
#res = sorted(res, key=itemgetter('rating'), reverse=True) 

#for i in res:
#    print(i)
