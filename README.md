Python script to retrieve your next HelloFresh delivery as a calendar entry served via an ics file.

Adding your email, password, and changing your locales should produce an ics file to be used in a calendar (served locally or via http).

For me setting cron the day before and during the delivery window is enough (no need to run it every 10 minutes throught the week):<br>
#delivery window wednesday 7:00 - 12:00, try https://crontab.guru/ if you need help<br>
0 12	    * * 2 /home/rondie/.scripts/hellofresh-delivery-ics.py
0,30 7-12	* * 3 /home/rondie/.scripts/hellofresh-delivery-ics.py
