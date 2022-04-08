import json
import jsonpath
from data.testData import baseUrl, endpoints
from services.requests import APIRequest
from utils.helpers import makePayload
from services.asserts import checkSuccessStatus


def test_successful_registration():
    v = baseUrl + endpoints["register"]
    x = APIRequest.postReqWithoutHeader(v, makePayload())
    checkSuccessStatus(x)


def test_fetch_user():
    v = baseUrl + endpoints["user"]
    x = APIRequest.get(v)
    responseJson = json.loads(x.text)
    checkSuccessStatus(x)
