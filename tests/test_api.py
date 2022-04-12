import json
import jsonpath
import pytest
from assertpy import assert_that

from factory.handle_process import (
    basic_post_req,
    basic_get_req,
    get_default_header,
    make_json_data,
)
from services.assertions.asserts import (
    check_success_status,
    check_bad_Request,
    load_json,
    check_response,
)
from services.rest_actions.requests import APIRequest
from test_data.constants import baseUrl, headers, wrong_user, user_janet
from test_data.endpoints import Endpoint


@pytest.mark.xfail
def test_successful_registration():
    """
    Test on hitting POST API, we'll create an user
    """
    req = basic_post_req("register")
    check_success_status(req)


def test_fetch_user():
    """
    Test on hitting GET API, we get a user named Janet
    """
    req = basic_get_req("user")
    check_success_status(req)
    req = json.dumps(req.text)
    assert_that(req).contains("Janet")


def test_read_all_has_Janet():
    """
    Test on hitting GET API, we get a user named Janet in the list of people
    """
    req = basic_get_req("user")
    check_success_status(req)
    check_response(req, "data", user_janet[0]["data"])
    data = load_json(req.text)
    assert data == user_janet[0]
    assert data["data"]["first_name"] == user_janet[0]["data"]["first_name"]
    assert jsonpath.jsonpath(data, "$.data.first_name")[0] == "Janet"
    assert jsonpath.jsonpath(data, "$.data.id")[0] == 2


def test_unsuccessfull_login():
    """
    Test on hitting POST API, for unsuccessfull login
    """
    makeUrl = baseUrl + Endpoint().get_endpoint()["login"]
    req = APIRequest().post(
        makeUrl,
        make_json_data(wrong_user["emailText"], wrong_user["emailData"]),
        get_default_header(headers["content_type"], headers["app_json"]),
    )
    check_bad_Request(req)
