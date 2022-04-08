import json
import random
import json
from time import time


def makePayload():
    data = json.loads(
        '{"email": "eve.holt@reqres.in","password": "' + randomDigits(5) + '"}'
    )
    return data


def randomDigits(digits):
    lower = 10 ** (digits - 1)
    upper = 10**digits - 1
    return str(random.randint(lower, upper))


def measure_time(function):
    start = time()
    result = function()
    end = time()
    return end - start, result
