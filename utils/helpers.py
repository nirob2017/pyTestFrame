import random
import json
from time import time
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()


@dataclass
class EnvironmentVars:
    """Return all secret environment variables"""

    Email = os.getenv("EMAIL")
    Password = os.getenv("PASS")
    APIKey = os.getenv("API_KEY")
    APIToken = os.getenv("API_TOKEN")


def make_payload():
    data = json.loads(
        '{"email": "eve.holt@reqres.in","password": "' + random_digits(5) + '"}'
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
