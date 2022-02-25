# HelloFresh Delivery ICS

Python script to retrieve your next HelloFresh delivery as a calendar entry served via an ics file.

Exporting your email, password, ics output path and changing your locales should produce an ics file to be used in a calendar (served locally or via http).

```
export HELLOFRESH_USERNAME='<username>'
export HELLOFRESH_PASSWORD='<password>'
export HELLOFRESH_ICS_PATH='<ics output path>'
```

Install required python3 packages:
```
pip3 install -r requirements.txt
```

For me setting cron the day before and during the delivery window is enough (no need to run it every 10 minutes throughout the week):
```
#delivery window wednesday 7:00 - 12:00, try https://crontab.guru/ if you need help
0 7	    * * 2 /home/rondie/.scripts/hellofresh-delivery-ics.py
0,30 7-12	* * 3 /home/rondie/.scripts/hellofresh-delivery-ics.py
```
