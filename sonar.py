import os
import time
import requests
import logging
from requests import ConnectionError

from configuration import *

debug = False
verbose = True
do_logging = True
version = "1.0.7"
working_frequency = 1
key_frequency = 'frequency'
key_verification = 'verification'
key_working_frequency = 'working_frequency'
default_frequency = 10 * 60 if not debug else 10
key_notification_mechanism_slack = "Slack-Notifier"
key_notification_mechanism_email = "Email-Notifier"
connectivity_verification_website = "https://www.google.com"
headers = {'user-agent': 'Website Sonar, version: ' + version}

elapsed_times = {}
for item in websites:
    elapsed_times[item] = 0


def log(what):
    if verbose:
        print what
    if do_logging:
        logging.info(what)


def check(website, configuration):
    if website != connectivity_verification_website:
        log("Checking:" + website)
    else:
        if debug:
            log("Checking for internet connection.")
    if "http" not in website:
        log("No schema defined for: " + website + ", falling back to default: http:// schema.")
        website = "http://" + website
    try:
        response = requests.get(website, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            return False
        body = response.text
        if key_verification in configuration:
            for criteria in configuration[key_verification]:
                if criteria not in body:
                    return False
    except ConnectionError:
        return False
    return True


def run(what):
    for cmd in what:
        os.system(cmd)


def alert(website):
    message = "Website check failed: " + website
    log(message)
    for mechanism in notification:
        if mechanism == key_notification_mechanism_slack:
            slack(message)
            continue
        if mechanism == key_notification_mechanism_email:
            email(message)
            continue
    return


def slack(message):
    command = [
        "python Slack/notify.py \"" + message + "\""
    ]
    if check(connectivity_verification_website, {}):
        run(command)


def email(message):
    command = [
        "python Email/notify.py \"" + message + "\""
    ]
    if check(connectivity_verification_website, {}):
        run(command)


def run_sonar():
    if do_logging:
        logging.basicConfig(
            filename="website-sonar.log",
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG
        )

    start_message = "Website Sonar (version: " + version + ") is STARTED."
    if key_notification_mechanism_email in notification:
        email(start_message)
    log(start_message)

    frequency = working_frequency
    if key_working_frequency in overrides:
        frequency = overrides[key_working_frequency]
    while True:
        time.sleep(frequency)
        for website in elapsed_times:
            elapsed_times[website] = elapsed_times[website] + frequency
            if debug:
                log("Tick. " + str(elapsed_times[website]))
            expected_frequency = default_frequency
            if key_frequency in websites[website]:
                expected_frequency = websites[website][key_frequency]
            if elapsed_times[website] >= expected_frequency:
                elapsed_times[website] = 0
                if not check(connectivity_verification_website, {}):
                    log("No internet connection available.")
                    continue
                if check(website, websites[website]):
                    log("Website " + website + " is OK.")
                else:
                    alert(website)


if __name__ == '__main__':
    run_sonar()
