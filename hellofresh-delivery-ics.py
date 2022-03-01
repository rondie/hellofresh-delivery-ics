#!/usr/bin/env python3

import json
import os
from datetime import datetime
from datetime import timedelta

import cloudscraper

from ics import Calendar, Event

requests = cloudscraper.create_scraper()

username = os.environ.get('HELLOFRESH_USERNAME')
password = os.environ.get('HELLOFRESH_PASSWORD')
url = 'https://www.hellofresh.nl'
icsfile = os.environ.get('HELLOFRESH_ICS_PATH')
addminutes = 15
country = 'nl'
locale = 'nl-NL'

# login page
loginurl = url + '/gw/login'
logindata = { 'username': username, 'password': password }
logindataJson = json.dumps(logindata, indent=4)

# token page
tokenpage = requests.post(loginurl, data = logindataJson)
tokenJson = json.loads(tokenpage.text)
tokenType = tokenJson['token_type']
token = tokenJson['access_token']
headers = {
            'Authorization': tokenType + ' ' + token
        }
params = dict()
params['country'] = country
params['locale'] = locale

# deliveries overview
deliverylinkurl = url + '/gw/api/customers/me/deliveries'
deliverylinkpage = \
    requests.get(deliverylinkurl, headers=headers, params=params)
deliverylinkJson = json.loads(deliverylinkpage.text)

# stop if no open deliveries 
if deliverylinkJson['items'][0]['tracking'] is None:
    print('no open deliveries')
    quit()

# delivery page with start time
deliveryurl = \
    deliverylinkJson['items'][0]['tracking']['tracking_link']
deliverystartstring = \
    deliverylinkJson['items'][0]['tracking']['estimated_delivery_time']
deliverystart = \
    datetime.strptime(deliverystartstring, "%Y-%m-%dT%H:%M:%S+0000")
# calculate the end time
deliveryend = deliverystart + timedelta(minutes=addminutes)

# ics event
c = Calendar()
e = Event()
e.name = 'Hellofresh'
e.begin = deliverystart
e.end = deliveryend
e.description = deliveryurl
c.events.add(e)
c.events
with open(icsfile, 'w') as my_file:
    my_file.writelines(c)
