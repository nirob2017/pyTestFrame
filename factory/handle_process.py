import json

from services.rest_actions.requests import APIRequest
from test_data.constants import user, baseUrl
from test_data.endpoints import Endpoint


def getDefaultHeader(key, value):
    header = {key: value}
    return header


def getPayload():
    payload = {user["email"], user["password"]}
    return payload


def basicGetReq(endpoint):
    makeUrl = baseUrl + Endpoint().get_endpoint()[endpoint]
    req = APIRequest().get(makeUrl)
    return req


def basicPostReq(endpoint):
    makeUrl = baseUrl + Endpoint().get_endpoint()[endpoint]
    req = APIRequest().post(f"{makeUrl}/getPayload()", getDefaultHeader())
    return req


def loadJson():
    data = json.dumps("email: peter@klaven")
    return data
