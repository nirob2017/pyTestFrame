import json
import jsonpath
import pytest
from assertpy import assert_that

from factory.handle_process import basicPostReq, basicGetReq, getDefaultHeader, loadJson
from services.assertions.asserts import (
    checkSuccessStatus,
    checkBadRequest,
    check_response,
)
from services.rest_actions.requests import APIRequest
from test_data.constants import baseUrl, headers
from test_data.endpoints import Endpoint


@pytest.mark.xfail
def test_successful_registration():
    """
    Test on hitting POST API, we'll create an user
    """
    req = basicPostReq("register")
    checkSuccessStatus(req)


def test_fetch_user():
    """
    Test on hitting GET API, we get a user named Janet
    """
    req = basicGetReq("user")
    checkSuccessStatus(req)
    req = json.dumps(req.text)
    assert_that(req).contains("Janet")


def test_read_all_has_Janet():
    """
    Test on hitting GET API, we get a user named Janet in the list of people
    """
    req = basicGetReq("user")
    responseJson = json.loads(req.text)
    checkSuccessStatus(req)
    assert jsonpath.jsonpath(responseJson, "$.data.first_name")[0] == "Janet"
    assert jsonpath.jsonpath(responseJson, "$.data.id")[0] == 2


def test_unsuccessfull_login():
    """
    Test on hitting POST API, for unsuccessfull login
    """
    makeUrl = baseUrl + Endpoint().get_endpoint()["login"]
    req = APIRequest().post(
        makeUrl,
        loadJson(),
        getDefaultHeader(headers["content_type"], headers["app_json"]),
    )
    checkBadRequest(req)
    check_response(req, "error", "Missing password")
