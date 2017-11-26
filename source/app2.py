#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask, url_for, jsonify
from flask import request
from flask import make_response, current_app
from functools import update_wrapper

from finnaircsvreader import findCoolCity

from get_images import get_pictures
from api_clarifai import get_predictions

from foursquaretest import findPlaces

import multiprocessing

#from phrase2vec import *



app = Flask(__name__)




def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def finair_data(date_start, date_end, budget):
    result = findCoolCity(date_start, date_end, budget)

    return result['destCity'], int(result['price'])

def get_city(x):
    date_start, date_end, budget = mstr.split(":")

    fcity, fprice = finair_data(date_start, date_end, budget)

    return {'city' : fcity}

import glob

def _process_one(x):
    print x
    account, city, query = x
    final_result = []

    flatten = lambda l: [item for sublist in l for item in sublist]
    if account == 'aewarfield':
        try:
            final_result.append(findPlaces(city, 'museum' + ' ' + query))
        except:
            pass
        try:
            final_result.append(findPlaces(city, 'theatre' + ' ' + query))
        except:
            pass
        try:
            final_result.append(findPlaces(city, 'restaurant' + ' ' + query))
        except:
            pass
        final_result = flatten(final_result)
        return final_result

    print 'wut'

    if account == 'juanixba':
        try:
            final_result.append(findPlaces(city, 'music' + ' ' + query))
        except:
            pass
        try:
            final_result.append(findPlaces(city, 'concert' + ' ' + query))
        except:
            pass
        try:
            final_result.append(findPlaces(city, 'bar' + ' ' + query))
        except:
            pass
        final_result = flatten(final_result)
        return final_result

    try:
        final_result.append(findPlaces(city, 'museum' + ' ' + query))
    except:    
        pass
    try:
        final_result.append(findPlaces(city, 'food' + ' ' + query))
    except:
        pass    
    try:
        final_result.append(findPlaces(city, 'music' + ' ' + query))
    except:
        pass    
    try:
        final_result.append(findPlaces(city, 'nature' + ' ' + query))
    except:
        pass    
    flatten = lambda l: [item for sublist in l for item in sublist]
    final_result = flatten(final_result)

    print 'wut3'

    return final_result

import uuid

def places_data(account, city):
    user_name = account
    n_pictures = 10

    pictures = get_pictures(user_name, n_pictures)

    print 'start image'
    predictions = get_predictions(pictures[:n_pictures])

    result = []
    for output in predictions['outputs']:
        concepts = output['data']['concepts']
        result.append([concept['name'] for concept in concepts])

    print 'start foursquare'
    rng = range(min(n_pictures, len(pictures)))

    x = zip([account for _ in rng], [city for _ in rng], [' '.join(result[i][:4]) for i in rng])
    print x
    pool = multiprocessing.Pool(8)
    final_result =  pool.map(_process_one, x)

    flatten = lambda l: [item for sublist in l for item in sublist]
    final_result = flatten(final_result)

    final_result = {v['name']:v for v in final_result}.values()

    final_result = list(filter(lambda x : float(x['rating']) > 5, final_result)) 
    final_result = list(filter(lambda x : ('store' not in x['category']) and ('Store' not in x['category']), final_result))
    for i in range(len(final_result)):
        final_result[i]['id'] = uuid.uuid4()

    return final_result

def get_topics(mstr):
    city = mstr

    result = dict()
    result['breakfast'] = (findPlaces(city, "breakfast"))
    result['museum'] = (findPlaces(city, "museum"))
    result['dinner'] = (findPlaces(city, "dinner"))
    result['nature'] = (findPlaces(city, "nature"))

    for i in range(len(result['breakfast'])):
        result['breakfast'][i]['id'] = uuid.uuid4()
    for i in range(len(result['museum'])):
        result['museum'][i]['id'] = uuid.uuid4()
    for i in range(len(result['dinner'])):
        result['dinner'][i]['id'] = uuid.uuid4()
    for i in range(len(result['nature'])):
        result['nature'][i]['id'] = uuid.uuid4()


    return result

def get_hotels(mstr):
    city = mstr

    result = dict()
    result['hotel'] = (findPlaces(city, "hotel"))

    return result

def get_places(mstr):
    date_start, date_end, budget, account = mstr.split(":")
    budget = int(budget)

    fcity, fprice = finair_data(date_start, date_end, budget)

    remain_budget = budget - fprice

    places = places_data(account, fcity)

    result = dict()
    result['city'] = fcity
    result['venues'] = places
    result['flight_price'] = fprice

    return result



@app.errorhandler(404)
def page_not_found(e):
    return 'Not a page.'

@app.route('/findair')
def api_ebutler():
    response = 0
    if 'get_topics' in request.args:
        response = jsonify(get_topics(request.args['get_topics']))
    elif 'get_hotels' in request.args:
        response = jsonify(get_hotels(request.args['get_hotels']))
    elif 'get_city' in request.args:
        reaponse = jsonify(get_city(request.args['get_cuty']))
    elif 'get_venues' in request.args:
        response = jsonify(get_places(request.args['get_venues']))
    else:
        response = jsonify(json.dumps(request.args))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

