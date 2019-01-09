import time

from configuration import *

debug = True

working_frequency = 1
key_frequency = 'frequency'

elapsed_times = {}
for website in websites:
    elapsed_times[website] = 0


def log(what):
    if debug:
        print what


def check(website, configuration):
    return True


def alert(website, configuration):
    return


while True:
    time.sleep(working_frequency)
    for website in elapsed_times:
        elapsed_times[website] = elapsed_times[website] + 1
        log("Website: " + website + ", elapsed: " + str(elapsed_times[website]))
        expected_frequency = 10 * 60
        if key_frequency in websites[website]:
            expected_frequency = websites[website][key_frequency]
        if elapsed_times[website] >= expected_frequency:
            elapsed_times[website] = 0
            if not check(website, websites[website]):
                alert(website, websites[website])



