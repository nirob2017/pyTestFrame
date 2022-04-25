import jsonpath
import pytest
from assertpy import assert_that

from conftest import EnvironmentVars
from factory.handle_process import (
    basic_post_req,
    basic_get_req,
    make_header,
    make_json_data,
)
from factory.handle_xml import XMLUtil
from services.assertions.asserts import Assertions
from factory.handle_json import JSONUtil
from services.rest_actions.requests import APIRequest
from test_data.constants import headers, user_janet
from test_data.endpoints import Endpoint


def test_successful_registration():
    """
    Test on hitting POST API, we'll create an user
    """
    req = basic_post_req("register")
    Assertions().check_response_status_created(req)


def test_fetch_user():
    """
    Test on hitting GET API, we get a user named Janet
    """
    req = basic_get_req(EnvironmentVars.BaseURL, Endpoint().get_endpoint()["user"])
    Assertions().check_success_status(req)
    req = JSONUtil.dump_json(req.text)
    assert_that(req).contains("Janet")


def test_read_all_has_Janet():
    """
    Test on hitting GET API, we get a user named Janet in the list of people
    """
    req = basic_get_req(EnvironmentVars.BaseURL, Endpoint().get_endpoint()["user"])
    Assertions().check_success_status(req)
    Assertions().check_response(req, "data", user_janet[0]["data"])
    data = JSONUtil.load_json(req.text)
    assert data == user_janet[0]
    assert data["data"]["first_name"] == user_janet[0]["data"]["first_name"]
    assert jsonpath.jsonpath(data, "$.data.first_name")[0] == "Janet"
    assert jsonpath.jsonpath(data, "$.data.id")[0] == 2


def test_unsuccessfull_login(invalid_user_data):
    """
    Test on hitting POST API, for unsuccessfull login
    """
    makeUrl = EnvironmentVars.BaseURL + Endpoint().get_endpoint()["login"]
    req = APIRequest().post(
        makeUrl,
        make_json_data(invalid_user_data["emailText"], invalid_user_data["emailData"]),
        make_header(headers["content_type"], headers["application_json"]),
    )
    Assertions().check_bad_Request(req)


@pytest.mark.parametrize("key, value", [("id", "761"), ("name", "Xim Cornel")])
def test_xml_response(key, value):
    """
    Test on hitting GET API, for testing xml response
    """

    req = APIRequest().get(EnvironmentVars.XmlURL)
    Assertions().check_success_status(req)
    xml_data = XMLUtil(req.text).convert_to_json_string()
    json_string = JSONUtil.dump_json(xml_data, indent=2, sort_keys=True)
    json_object = JSONUtil.load_json(json_string)
    for k, v in json_object.items():
        for m, n in json_object[k]["travelers"].items():
            for dic in n:
                for val, cal in dic.items():
                    assert n[0][key] == value

    assert (
        json_object["TravelerinformationResponse"]["travelers"]["Travelerinformation"][
            0
        ]["name"]
        == "Xim Cornel"
    )
