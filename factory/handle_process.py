from conftest import EnvironmentVars
from factory.handle_json import JSONUtil
from services.rest_actions.requests import APIRequest
from test_data.constants import Constants
from test_data.endpoints import Endpoint


def make_header(key, value):
    header = {key: value}
    return header


def make_payload(**data):
    payload_data = JSONUtil().dump_json(data)
    return payload_data


def make_user_payload():
    payload = {Constants().user["email"], Constants().user["password"]}
    return payload


def basic_get_req(url, endpoint):
    makeUrl = url + endpoint
    req = APIRequest().get(makeUrl)
    return req


def basic_post_req(endpoint):
    makeUrl = EnvironmentVars.BaseURL + Endpoint().get_endpoint()[endpoint]
    req = APIRequest().post(
        f"{makeUrl}/getPayload()",
        make_header(
            Constants().headers["content_type"], Constants().headers["application_json"]
        ),
    )
    return req


def make_json_data(key, value):
    data = JSONUtil.dump_json(f"${key}" + ":" f"${value}")
    return data


def header_with_bearer_token():
    return make_header(
        Constants().headers["authentication"],
        Constants().headers["bearer"] + Constants().token,
    )
