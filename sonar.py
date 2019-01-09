import time

from configuration import *

debug = True

# Working frequency is 1 second.
working_frequency = 1

elapsed_times = {}
for website in websites:
    elapsed_times[website] = 0


def log(what):
    if debug:
        print what


while True:
    time.sleep(working_frequency)
    for website in elapsed_times:
        elapsed_times[website] = elapsed_times[website] + 1
        log("Website: " + website + ", elapsed: " + str(elapsed_times[website]))
