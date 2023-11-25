import json
import sys
from datetime import datetime, time, timedelta
from os.path import exists

from apscheduler.schedulers.background import BackgroundScheduler

import cloudscraper

from config import addminutes, debug, icsfile, icsname, params, \
        password, sessionfile, timezone, url, username

from ics import Calendar, Event

scraper = cloudscraper.create_scraper()
now = datetime.now()
seconds_array = [600, 1800, 7200, 86400]


scheduler = BackgroundScheduler({'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '1'
    }
})


# use existing session if not expired
def testsession():
    if exists('hellofreshsession.py'):
        from hellofreshsession import expires_at
        if expires_at < now.timestamp():
            token, token_type = getsession()
        else:
            from hellofreshsession import token, token_type
    else:
        token, token_type = getsession()
    return token, token_type


def getsession():
    # login data
    login_url = url + '/gw/login'
    login_data = {'username': username, 'password': password}
    login_data_json = json.dumps(login_data, indent=4)
    # get access token
    try:
        token_page = scraper.post(login_url,
                                  data=login_data_json,
                                  params=params
                                  )
        token_page.raise_for_status()
    except Exception as err:
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


def get_deliveries():
    token, token_type = testsession()
    headers = {'Authorization': token_type + ' ' + token}
    delivery_link_url = url + '/gw/api/customers/me/deliveries'
    try:
        delivery_link_page = \
            scraper.get(delivery_link_url, headers=headers, params=params)
        delivery_link_page.raise_for_status()
    except Exception as err:
        print("Retrieve deliveries failed")
        print(err)
        sys.exit(1)
    delivery_link_json = json.loads(delivery_link_page.text)
    global delivery_data
    delivery_data = []
    for entry in delivery_link_json['items']:
        tz = datetime.strptime(
                entry['deliveryDate'], "%Y-%m-%dT%H:%M:%S%z").tzinfo
        if entry['tracking']:
            # given time offset is not ISO8601 compliant (+0000)
            # so we cut it off
            begin = datetime.fromisoformat(
                entry['tracking']['estimated_delivery_time'][:19])
            end = begin + timedelta(minutes=addminutes)
            description = entry['product']['productName']\
                + '\n' + entry['tracking']['tracking_link']
        else:
            day = datetime.strptime(entry['deliveryDate'],
                                    "%Y-%m-%dT%H:%M:%S%z").date()
            begin = datetime.combine(
                day, time.fromisoformat(
                    entry['deliveryOption']['deliveryFrom']), tzinfo=tz)
            end = datetime.combine(
                    day,
                    time.fromisoformat(entry['deliveryOption']['deliveryTo']),
                    tzinfo=tz)
            description = entry['product']['productName']
        delivery_data.append({
            'begin': begin,
            'end': end,
            'description': description})
    if debug:
        print("DEBUG: retrieved", len(delivery_data), "delivery dates")
    return delivery_data


def create_ics(icsfile):
    # create ics file
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
    if debug:
        print("DEBUG: file", icsfile, "written")


def next_delivery():
    # get nearest delivery date
    delivery_data_begin = []
    for entry in delivery_data:
        if entry['begin'].timestamp() > now.timestamp():
            delivery_data_begin.append({entry['begin']})
    delivery_data_nearest = next(iter(min(delivery_data_begin)))
    if debug:
        print("DEBUG: next delivery at", delivery_data_nearest)
    return (delivery_data_nearest)


def seconds_offset(seconds_array):
    delivery = next_delivery()
    seconds_until_delivery = (delivery.replace(tzinfo=None) -
                              datetime.fromtimestamp(now.timestamp()).replace(
                                  second=0,
                                  microsecond=0
                                  )).total_seconds()
    time_offset = []
    for sec in seconds_array:
        if sec < seconds_until_delivery:
            time_offset.append(sec)
    if debug:
        print("DEBUG: schedule", max(time_offset),
              "seconds before next delivery")
    return max(time_offset)


def fetch_hf_data():
    try:
        get_deliveries()
    except Exception:
        run_date = now + timedelta(seconds=600)
        scheduler.add_job(
            fetch_hf_data,
            'date',
            run_date=run_date
        )
        if debug:
            print("DEBUG: retrieve failed, next try scheduled at", run_date)
    else:
        create_ics(icsfile)
        delivery = next_delivery()
        run_date = delivery - timedelta(seconds=seconds_offset(seconds_array))
        scheduler.add_job(
            fetch_hf_data,
            'date',
            run_date=run_date
        )
        if debug:
            print("DEBUG: next run scheduled at", run_date)


def read_ics(icsfile):
    file = open(icsfile, 'r')
    events = []
    cal = file.read()
    c = Calendar(cal)
    for e in sorted(c.events):
        name = e.description
        begin = e.begin.to(timezone).format('DD-MM-YYYY HH:mm')
        end = e.end.to(timezone).format('HH:mm')
        events.append((name, begin, end))
    return (events)
    file.close()
