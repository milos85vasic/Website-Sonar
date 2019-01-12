# Website Sonar

Tool used to periodically ping associated websites and trigger alarm if website is unavailable.

## How to use

- Make sure [Requests](http://docs.python-requests.org/en/latest/) python library is installed on your system
- Make sure that [Slack Python API](https://github.com/slackapi/python-slackclient) is installed
- Clone the project
- Initialize and clone all git submodules
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

overrides = {}
```

Where 'websites' represents dictionary with sonar urls as keys and configurations as value pairs.
Each configuration contains:
    
1. 'verification', list of strings to search for verification (if any of strings from the list is not found in url's response, sonar considers check as failure)
2. 'frequency', check frequency in seconds.

Websites without 'verification' values will not check against verification strings.
Websites without 'frequency' value will be checked on every 10 minutes (default value).

'notification' list represents the list of notification mechanisms that will be used to notify users about unreachable website.

There are two notification mechanism supported: [Slack Notifier](https://github.com/milos85vasic/Slack-Notifier) and
 [Email Notifier](https://github.com/milos85vasic/Email-Notifier).

- Start website sonar:
```
$ python sonar.py
```

or

```
$ python sonar.py &
```

or with Venv (example):

```
$ source path_to_your_venv/bin/activate; cd ~/website-sonar; python ~/website-sonar/sonar.py &
```

Some parameters can be overriden. For example if we define overrides in our configuration.py:

```python
overrides = {
    "working_frequency": 10
}
```

Website sonar's timer will tick on every 10 seconds.