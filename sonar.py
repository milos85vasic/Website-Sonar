import time
import requests

from configuration import *

debug = True
verbose = True
working_frequency = 1
key_frequency = 'frequency'
key_verification = 'verification'
default_frequency = 10 * 60 if not debug else 10

elapsed_times = {}
for item in websites:
    elapsed_times[item] = 0


def log(what):
    if verbose:
        print what


def check(website, configuration):
    log("Checking: " + website)
    if "http" not in website:
        log("No schema defined for: " + website + ", falling back to default: http:// schema.")
        website = "http://" + website
    response = requests.get(website)
    if response.status_code != 200 and response.status_code != 201:
        return False
    body = response.text
    if key_verification in configuration:
        for criteria in configuration[configuration][key_verification]:
            if criteria not in body:
                return False
    return True


def alert(website, configuration):
    log("Website check failed: " + website)
    return


def run_sonar():
    while True:
        time.sleep(working_frequency)
        for website in elapsed_times:
            elapsed_times[website] = elapsed_times[website] + 1
            expected_frequency = default_frequency
            if key_frequency in websites[website]:
                expected_frequency = websites[website][key_frequency]
            if elapsed_times[website] >= expected_frequency:
                elapsed_times[website] = 0
                if not check(website, websites[website]):
                    alert(website, websites[website])


if __name__ == '__main__':
    run_sonar()
