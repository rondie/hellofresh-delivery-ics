# HelloFresh Delivery ICS

Python script to retrieve your next HelloFresh delivery as a calendar entry served via an ics file.

Exporting your email, password, ics output path and changing your locales should produce an ics file to be used in a calendar (served locally or via http).

```
export HELLOFRESH_USERNAME='<username>'
export HELLOFRESH_PASSWORD='<password>'
export HELLOFRESH_ICS_PATH='<ics output path>'
```

# CRON
Install required python3 packages:
```
pip3 install -r requirements.txt
```

For me setting cron the day before and during the delivery window is enough (no need to run it every 10 minutes throughout the week):
```
#delivery window wednesday 7:00 - 12:00, try https://crontab.guru/ if you need help
0 7	  * * 2 HELLOFRESH_USERNAME='user' HELLOFRESH_PASSWORD='pass' HELLOFRESH_ICS_PATH='/tmp/file.ics' /home/rondie/.scripts/hellofresh-delivery-ics.py
0,30 7-12 * * 3 HELLOFRESH_USERNAME='user' HELLOFRESH_PASSWORD='pass' HELLOFRESH_ICS_PATH='/tmp/file.ics' /home/rondie/.scripts/hellofresh-delivery-ics.py
```

# Daemon
Environment variable 'HELLOFRESH_ICS_DAEMON=true' will start an HTTP server serving http://<host>/hellofresh-delivery.ics. It will also update the ics file before the next delivery time as it draws nearer.

Environment variables that can be set:
| Name | default |
| ---- | ------- |
| HVC_ICS_HOST | 0.0.0.0 |
| HVC_ICS_PORT | 5000 |
| HVC_ICS_WORKERS | 1 |
| HVC_ICS_THREADS | 1 |
| HVC_ICS_TIMEOUT | 10 |

# Debug
Environment variable 'HELLOFRESH_ICS_DEBUG=true' will output taken actions
