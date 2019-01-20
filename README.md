# Website Sonar

Tool used to periodically ping associated websites and trigger alarm if website is unavailable.

## How to use

- Make sure [Requests](http://docs.python-requests.org/en/latest/) python library is installed on your system
- Make sure that [Slack Python API](https://github.com/slackapi/python-slackclient) is installed
- Clone the project
- Initialize and clone all git submodules
- In project root create JSON with the following structure (as int the example):

```json
{
  "websites": [
      {
        "url": "www.fundamental-kotlin.com",
        "frequency": 20,
        "verification": [
          "What is Kotlin?"
        ]
      },
      {
        "url": "https://www.damodred.com"
      },
      {
        "url": "https://www.irichanin.com",
        "frequency": 20,
        "verification": [
          "Agricultural holding Irichanin",
          "Proudly powered by WordPress"
        ]
      },
      {
        "url": "http://www.kolekcionari.rs"
      }
    ],
    "notification": [
      "Slack-Notifier",
      "Email-Notifier"
    ],
    "overrides": {
      "working_frequency": 10,
      "connectivity_verification_website": "https://www.example.com"
    }
}
```

Where 'websites' represents list with website configurations.
Each configuration contains:
    
1. 'url', website url
2. 'verification', list of strings to search for verification (if any of strings from the list is not found in url's response, sonar considers check as failure)
3. 'frequency', check frequency in seconds.

Websites without 'verification' values will not check against verification strings.
Websites without 'frequency' value will be checked on every 10 minutes (default value).

'notification' list represents the list of notification mechanisms that will be used to notify users about unreachable website.

There are two notification mechanism supported: [Slack Notifier](https://github.com/milos85vasic/Slack-Notifier) and
 [Email Notifier](https://github.com/milos85vasic/Email-Notifier).
 
NOTE: Overriding 'connectivity_verification_website' parameter is mandatory!

- Start website sonar:

(configuration file 'configuration.json' will be used)
```
$ python sonar.py
```

or

(configuration file 'my_configuration.json' will be used)
```
$ python sonar.py --configuration="my_configuration"
```

or with Venv (example):

(configuration file 'configuration.json' will be used)
```
$ source path_to_your_venv/bin/activate; cd ~/website-sonar; python ~/website-sonar/sonar.py &
```

Some parameters can be overridden. For example if we define overrides in our configuration.py:

```json
{
  "overrides": {
      "working_frequency": 10,
      "connectivity_verification_website": "https://www.example.com"
  }
}
```

Website sonar's timer will tick on every 10 seconds and 'https://www.example.com' will be pinged for connectivity checks.