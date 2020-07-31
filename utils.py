import json
import multiprocessing
import math
import time
import base64
import csv
import os
import sys
import copy
import requests
import datetime
import random

# Klaviyo
def send_event_payload(payload):
    '''
    input: payload of event object
    output: None (successfully sent) or unencoded payload (on failure)
    action: sends a complete event payload (including key) to events api, after formatting timestamp and event_id according to docs
    '''

    payload = set_event_id(payload)
    payload = set_timestamp(payload)

    endpoint = 'https://a.klaviyo.com/api/track'

    encoded_payload = base64.b64encode(json.dumps(payload).encode('utf-8'))

    params = {'data': encoded_payload}

    while True:

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:

            return None

        elif response.status_code == 429:

            time.sleep(10)

        else:

            return payload


def send_profile_payload(payload):
    '''
    input: payload of profile object
    output: None (successfully sent) or unencoded payload (on failure)
    action: sends a complete profile payload (including key) to identify api 
    '''

    endpoint = 'https://a.klaviyo.com/api/identify'

    encoded_payload = base64.b64encode(json.dumps(payload).encode('utf-8'))

    params = {'data': encoded_payload}

    while True:

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:

            return None

        elif response.status_code == 429:

            time.sleep(10)

        else:

            return payload

def set_timestamp(payload):
    '''
    input: payload for event
    ouput: an updated payload
    action: sets event "time" according to logic laid out in docs
    '''

    if 'time' not in payload.keys():
        payload['time'] = int(time.time())
    elif payload['time'].isnumeric():
        payload['time'] = int(payload['time'])
    else:
        payload['time'] = int(datetime.datetime.fromisoformat(payload['time']).timestamp())

    return payload


def set_event_id(payload):
    '''
    input: payload for event
    ouput: an updated payload
    action: sets $event_id according to logic laid out in docs
    '''

    if '$event_id' not in payload.keys():

        payload['$event_id'] = abs(hash(str(payload)))

    elif not payload['$event_id']:

            del payload['$event_id']

            payload['$event_id'] = abs(hash(str(payload)))

    return payload


def csv_to_payloads(public_key, mapping, filepath):
    '''
    input: config.public_key, config.mapping, filepath
    output: list of payloads (either events or profiles, depending on chosen mapping)
    action: converts CSV data to list of json objects
    '''

    # get data and headers into list of lists
    with open(filepath,'r',encoding='utf-8-sig') as f:

        reader = csv.reader(f)

        data = list(reader)

    headers = data.pop(0)

    # name to col
    name_to_col = {}
    for i in range(len(headers)):

        name_to_col[headers[i]]=i

    # create list of json objs

    objs = []

    for row in data:

        obj = copy.deepcopy(mapping)
        keys = list(obj.keys())

        for key in keys:

            if key == 'event':

                continue

            elif type(obj[key]) == str:

                value = row[name_to_col[obj[key]]]

                if value != '':

                    obj[key] = value

                else:

                    del obj[key]

            elif type(obj[key]) == dict:

                subkeys = list(obj[key].keys())

                for subkey in subkeys:
                    
                    value = row[name_to_col[obj[key][subkey]]]

                    if value != '':

                        obj[key][subkey] = value

                    else:

                        del obj[key][subkey]

            else:

                print('ERROR: neither string nor dict')
                return False

        obj['token'] = public_key

        if 'event' in mapping.keys():
            obj['event'] = mapping['event']

        objs.append(copy.deepcopy(obj))

    return objs



# Threading
def parallelize(function,args):
    '''
    input: function, list of args
    output: list of outputs from function applied to each arg
    '''

    cores = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=cores)

    outputs = pool.map(function,args)

    return outputs









