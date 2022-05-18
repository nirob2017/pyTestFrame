import random
import json
from time import time
from dotenv import load_dotenv

from conftest import EnvironmentVars
from factory.handle_process import header_with_bearer_token, make_header
from services.rest_actions.requests import APIRequest
from test_data.constants import Constants
from test_data.endpoints import Endpoint

load_dotenv()


def make_email_payload():
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


def nifty_auth_get_request(endpoint, param=None):
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint(endpoint),
        header_with_bearer_token(),
        params=param,
    )
    return req


def nifty_get_request(endpoint, param=None):
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint(endpoint),
        make_header(
            Constants().headers["content_type"], Constants().headers["app_x_encoded"]
        ),
        params=param,
    )
    return req
