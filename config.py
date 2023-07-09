#!/usr/bin/env python3

import os
import sys

username = os.environ.get('HELLOFRESH_USERNAME')
password = os.environ.get('HELLOFRESH_PASSWORD')
url = os.environ.get('HELLOFRESH_ICS_URL','https://www.hellofresh.nl')
sessionfile = 'hellofreshsession.py'
country = os.environ.get('HELLOFRESH_ICS_COUNTRY','nl')
locale = os.environ.get('HELLOFRESH_ICS_LOCALE','nl-NL')

icsfile = os.environ.get('HELLOFRESH_ICS_FILENAME', "hellofresh-delivery.ics")
addminutes = 15
icsname = 'HelloFresh Delivery'

debug = os.environ.get('HELLOFRESH_ICS_DEBUG',
                       'false').lower() in ('true', '1', 't')

host = os.environ.get("HELLOFRESH_ICS_HOST", "0.0.0.0")
port = os.environ.get("HELLOFRESH_ICS_PORT", 5000)
workers = os.environ.get("HELLOFRESH_ICS_WORKERS", 1)
threads = os.environ.get("HELLOFRESH_ICS_THREADS", 1)
timeout = os.environ.get("HELLOFRESH_ICS_TIMEOUT", 10)

bind = f"{host}:{port}"
workers = f"{workers}"
threads = f"{threads}"
timeout = f"{timeout}"

# test for input
if not username or not password:
    print("Need vars HELLOFRESH_USERNAME and HELLOFRESH_PASSWORD")
    sys.exit(1)
