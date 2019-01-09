# Website Sonar

Tool used to periodically ping associated websites and trigger alarm if website is unavailable.

## How to use

- Clone the project
- In project root create configuration.py with the following structure (as example):

```python
websites = {
    "https://www.damodred.com": {},
    "https://www.irichanin.com": {
        "verification": [
            "Agricultural holding Irichanin",
            "Proudly powered by WordPress"
        ],
        "frequency": 120
    },
    "http://www.kolekcionari.rs": {},
    "www.fundamental-kotlin.com": {}
}

notification = ["Slack-Notifier", "Email-Notifier"]
```

Where 'websites' represents dictionary with sonar urls as keys and configurations as value pairs.
Each configuration contains:
    
1. 'verification', list of strings to search for verification (if any of strings from the list is not found in url's response, sonar considers check as failure)
2. 'frequency', check frequency in seconds.

Websites without 'verification' values will not check against verification strings.
Websites without 'frequency' value will be checked on every 10 minutes (default value).

'notification' list represents the list of notification mechanisms that will be used to notify users about unreachable website.

For now only [Slack Notifier](https://github.com/milos85vasic/Slack-Notifier) is supported.

- Start website sonar:
```
$ python sonar.py
```

or

```
$ python sonar.py &
```
