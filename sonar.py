import os
import sys
import time
import json
import urllib2
import requests
import logging
import os.path

from requests import ConnectionError
from logging.handlers import RotatingFileHandler

param_configuration_name = '--configuration'
configuration_default_file = 'configuration.json'

configuration = {}
key_websites = 'websites'
key_overrides = 'overrides'
key_notification = 'notification'
key_connectivity_verification_website = 'connectivity_verification_website'


def load_configuration():
    configuration_file = configuration_default_file
    for arg in sys.argv:
        if sys.argv.index(arg) > 0:
            if param_configuration_name in arg:
                configuration_name = arg.replace(param_configuration_name, "")
                configuration_name = configuration_name.replace(".json", "")
                configuration_name = configuration_name.replace("=", "")
                configuration_name = configuration_name.replace("'", "")
                configuration_name = configuration_name.replace("\"", "")
                configuration_name = configuration_name.replace(" ", "")
                configuration_file = configuration_name + ".json"

    log("Starting Website Sonar (version: " + version + "). Configuration file: " + configuration_file + ".")
    if os.path.isfile(configuration_file):
        try:
            json_file = open(configuration_file)
            json_str = json_file.read()
            configuration.update(json.loads(json_str))
            if key_websites in configuration and key_overrides in configuration and \
                    key_connectivity_verification_website in configuration[key_overrides]:
                return True
        except:
            return False
    return False


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
headers = {'user-agent': 'Website Sonar, version: ' + version}

log_filename = 'website-sonar.log'
log_files_count = 10 if not debug else 5
log_max_file_size = 5 * 1024 * 1024 if not debug else 1024

elapsed_times = {}
for item in configuration[key_websites]:
    elapsed_times[item] = 0

unreachable_websites = []


def log(what):
    if verbose:
        print what
    if do_logging:
        app_log.info(what)


def internet_on():
    try:
        urllib2.urlopen(configuration[key_overrides][key_connectivity_verification_website], timeout=1)
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
    if check(website, configuration[key_websites][website]):
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
    if key_notification in configuration:
        for mechanism in configuration[key_notification]:
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

    if not load_configuration():
        log("Website Sonar (version: " + version + ") could not be started. Could not load configuration JSON.")
        sys.exit(1)

    start_message = "Website Sonar (version: " + version + ") is STARTED."
    if key_notification in configuration and key_notification_mechanism_email in configuration[key_notification]:
        email(start_message)
    log(start_message)

    frequency = working_frequency
    if key_working_frequency in configuration[key_overrides]:
        frequency = configuration[key_overrides][key_working_frequency]

    while True:
        time.sleep(frequency)
        for website in elapsed_times:
            elapsed_times[website] = elapsed_times[website] + frequency
            if debug:
                log("Tick. " + str(elapsed_times[website]))
            expected_frequency = default_frequency
            if key_frequency in configuration[key_websites][website]:
                expected_frequency = configuration[key_websites][website][key_frequency]
            if elapsed_times[website] >= expected_frequency:
                elapsed_times[website] = 0
                if not internet_on():
                    log("No internet connection available.")
                    continue

                perform_check(website)


if __name__ == '__main__':
    run_sonar()
