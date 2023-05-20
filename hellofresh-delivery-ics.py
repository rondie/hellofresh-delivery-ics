#!/usr/bin/env python3

import json
import sys
from datetime import datetime, time, timedelta
from os.path import exists

import cloudscraper

from config import addminutes, country, icsfile, \
    icsname, locale, password, sessionfile, url, username

from ics import Calendar, Event

requests = cloudscraper.create_scraper()
now = datetime.now().timestamp()


def getsession():
    # login data
    login_url = url + '/gw/login'
    login_data = {'username': username, 'password': password}
    login_data_json = json.dumps(login_data, indent=4)
    # get access token
    try:
        token_page = requests.post(login_url, data=login_data_json)
        token_page.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Login failed, check credentials")
        print(err)
        sys.exit(1)
    token_json = json.loads(token_page.text)
    token_type = token_json['token_type']
    token = token_json['access_token']
    expires_at = token_json['issued_at'] + token_json['expires_in']
    # write session data to file
    f = open(sessionfile, "w")
    f.write(f"token_type = \
        '{token_type}'\ntoken = '{token}'\nexpires_at = {expires_at}")
    f.close()
    return token, token_type


# use existing session if not expired
if exists('hellofreshsession.py'):
    from hellofreshsession import expires_at
    if expires_at < now:
        token, token_type = getsession()
    else:
        from hellofreshsession import token, token_type
else:
    token, token_type = getsession()

headers = {
            'Authorization': token_type + ' ' + token
        }
params = dict()
params['country'] = country
params['locale'] = locale

# deliveries overview
delivery_link_url = url + '/gw/api/customers/me/deliveries'
try:
    delivery_link_page = \
        requests.get(delivery_link_url, headers=headers, params=params)
    delivery_link_page.raise_for_status()
except requests.exceptions.HTTPError as err:
    print("Retrieve deliveries failed")
    print(err)
    sys.exit(1)
delivery_link_json = json.loads(delivery_link_page.text)
delivery_data = []
for entry in delivery_link_json['items']:
    tz = datetime.strptime(entry['deliveryDate'], "%Y-%m-%dT%H:%M:%S%z").tzinfo
    if entry['tracking']:
        # given time offset is not ISO8601 compliant (+0000), so we cut it off
        begin = datetime.fromisoformat\
            (entry['tracking']['estimated_delivery_time'][:19])
        end = begin + timedelta(minutes=addminutes)
        description = entry['product']['productName'] + '\n' + entry['tracking']['tracking_link']
    else:
        day = datetime.strptime(entry['deliveryDate'], "%Y-%m-%dT%H:%M:%S%z").date()
        begin = datetime.combine(day, time.fromisoformat(entry['deliveryOption']['deliveryFrom']), tzinfo=tz)
        end = datetime.combine(day, time.fromisoformat(entry['deliveryOption']['deliveryTo']), tzinfo=tz)
        description = entry['product']['productName']
    delivery_data.append({
        'begin': begin,
        'end': end,
        'description': description
        })


def createics(icsfile):
    with open(icsfile, 'w') as my_file:
        # ics event
        c = Calendar()
        for entry in delivery_data:
            e = Event()
            e.name = icsname
            e.begin = entry['begin']
            e.end = entry['end']
            e.description = entry['description']
            c.events.add(e)
        c.events
        my_file.writelines(c)


def nextrun(delivery_data):
    delivery_data_begin = []
    for entry in delivery_data:
        delivery_data_begin.append({entry['begin']})
    delivery_data_nearest = min(delivery_data_begin)
    return(delivery_data_nearest)


if icsfile:
    createics(icsfile)


nextrun(delivery_data)
