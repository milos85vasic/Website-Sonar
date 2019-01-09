import time

from configuration import *

debug = True
verbose = True
working_frequency = 1
key_frequency = 'frequency'
default_frequency = 10 * 60 if not debug else 10

elapsed_times = {}
for website in websites:
    elapsed_times[website] = 0


def log(what):
    if verbose:
        print what


def check(website, configuration):
    log("Checking: " + website)
    return True


def alert(website, configuration):
    log("Website check failed: " + website)
    return


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
