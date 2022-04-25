import random
import json
from time import time
from dotenv import load_dotenv

from conftest import EnvironmentVars

load_dotenv()


def make_payload():
    data = json.loads(
        '{"email":' + EnvironmentVars.Email + ',"password": "' + random_digits(5) + '"}'
    )
    return data


def random_digits(digits):
    lower = 10 ** (digits - 1)
    upper = 10**digits - 1
    return str(random.randint(lower, upper))


def measure_time(function):
    start = time()
    result = function()
    end = time()
    return end - start, result
