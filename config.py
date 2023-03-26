#!/usr/bin/env python3

import os

username = os.environ.get('HELLOFRESH_USERNAME')
password = os.environ.get('HELLOFRESH_PASSWORD')
url = 'https://www.hellofresh.nl'
sessionfile = 'hellofreshsession.py'
country = 'nl'
locale = 'nl-NL'

icsfile = os.environ.get('HELLOFRESH_ICS_PATH')
addminutes = 15
icsname = 'HelloFresh Delivery'

# test for input
if not username or not password:
    print("Need vars HELLOFRESH_USERNAME and HELLOFRESH_PASSWORD")
    sys.exit(1)

