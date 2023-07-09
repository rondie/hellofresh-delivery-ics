# HelloFresh Delivery ICS

Container to retrieve your next HelloFresh delivery as a calendar entry served via an ics file. It will fetch new data as the next delivery date gets nearer.

Exporting your email and password should produce an ics file serverd through http to be used in a calendar.

```
export HELLOFRESH_USERNAME='<username>'
export HELLOFRESH_PASSWORD='<password>'
```


Environment variables that can be set:
| Name | default |
| ---- | ------- |
| HELLOFRESH_ICS_WORKERS | 1 |
| HELLOFRESH_ICS_THREADS | 1 |
| HELLOFRESH_ICS_TIMEOUT | 10 |
| HELLOFRESH_ICS_FILENAME | hellofresh-delivery.ics |
| HELLOFRESH_ICS_UID | 1000 |
| HELLOFRESH_ICS_GID | 1000 |
| HELLOFRESH_ICS_URL | https://www.hellofresh.nl |
| HELLOFRESH_ICS_COUNTRY | nl |
| HELLOFRESH_ICS_LOCALE | nl-NL |

Container runs on port 5000.

# Debug
Environment variable 'HELLOFRESH_ICS_DEBUG=true' will output taken actions
