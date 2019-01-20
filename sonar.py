import os
import time
import urllib2
import requests
import logging

from requests import ConnectionError
from logging.handlers import RotatingFileHandler

from configuration import *

app_log = logging.getLogger('root')

debug = False
verbose = True
do_logging = True
version = "1.2.0"
working_frequency = 1
key_frequency = 'frequency'
key_verification = 'verification'
key_working_frequency = 'working_frequency'
default_frequency = 10 * 60 if not debug else 10
key_notification_mechanism_println = "Println"
key_notification_mechanism_slack = "Slack-Notifier"
key_notification_mechanism_email = "Email-Notifier"
connectivity_verification_website = "https://www.google.com"
headers = {'user-agent': 'Website Sonar, version: ' + version}

log_filename = 'website-sonar.log'
log_files_count = 10 if not debug else 5
log_max_file_size = 5 * 1024 * 1024 if not debug else 1024

elapsed_times = {}
for item in websites:
    elapsed_times[item] = 0

unreachable_websites = []


def log(what):
    if verbose:
        print what
    if do_logging:
        app_log.info(what)


def internet_on():
    try:
        urllib2.urlopen(connectivity_verification_website, timeout=1)
        return True
    except urllib2.URLError:
        return False


def check(website, configuration):
    log("Checking: " + website)
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


def perform_check(website):
    if check(website, websites[website]):
        message = "Website " + website + " is ok."
        if website in unreachable_websites:
            message = "Website " + website + " is reachable again."
            unreachable_websites.remove(website)
            notify(message)

        log(message)
    else:
        if website not in unreachable_websites:
            fail(website)
        else:
            log("Website is still not reachable: " + website)


def run(what):
    for cmd in what:
        os.system(cmd)


def fail(website):
    unreachable_websites.append(website)
    message = "Website is not reachable: " + website
    log(message)
    notify(message)
    return


def notify(message):
    for mechanism in notification:
        if mechanism == key_notification_mechanism_slack:
            slack(message)
            continue
        if mechanism == key_notification_mechanism_email:
            email(message)
            continue
        if mechanism == key_notification_mechanism_println:
            print ("MSG :: " + message)
            continue


def slack(message):
    command = [
        "python Slack/notify.py \"" + message + "\""
    ]
    if internet_on():
        run(command)


def email(message):
    command = [
        "python Email/notify.py \"" + message + "\""
    ]
    if internet_on():
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

        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

        handler = RotatingFileHandler(
            log_filename, mode='a', maxBytes=log_max_file_size, backupCount=log_files_count, encoding=None, delay=0
        )

        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)

        app_log.setLevel(logging.DEBUG)
        app_log.addHandler(handler)

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
                if not internet_on():
                    log("No internet connection available.")
                    continue

                perform_check(website)


if __name__ == '__main__':
    run_sonar()
