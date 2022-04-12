import json

from services.rest_actions.requests import APIRequest
from test_data.constants import user, baseUrl
from test_data.endpoints import Endpoint


def get_default_header(key, value):
    header = {key: value}
    return header


def get_payload():
    payload = {user["email"], user["password"]}
    return payload


def basic_get_req(endpoint):
    makeUrl = baseUrl + Endpoint().get_endpoint()[endpoint]
    req = APIRequest().get(makeUrl)
    return req


def basic_post_req(endpoint):
    makeUrl = baseUrl + Endpoint().get_endpoint()[endpoint]
    req = APIRequest().post(f"{makeUrl}/getPayload()", get_default_header())
    return req


def make_json_data(key, value):
    data = json.dumps(f"${key}" + ":" f"${value}")
    return data
