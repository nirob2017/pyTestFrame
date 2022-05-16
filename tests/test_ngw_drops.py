from conftest import EnvironmentVars
from factory.handle_json import JSONUtil
from factory.handle_process import make_header, basic_get_req
from services.assertions.asserts import Assertions
from services.rest_actions.requests import APIRequest
from test_data.constants import Constants
from test_data.endpoints import Endpoint


def test_curated_drop_schedule():
    param = {"listing_type": "curated"}
    schedule_req = ngw_get_req_with_param("drop_schedule", param)
    # Asserting response status code, response
    Assertions().check_success_status(schedule_req)
    Assertions().assert_response_with_expected_result(
        schedule_req, "message", "Schedule items retrieved"
    )
    schedule_items = JSONUtil().find_values_from_json_using_key(
        "scheduleItems", schedule_req.text
    )
    if len(schedule_items) != 0:
        Assertions().assert_response_with_expected_result(
            schedule_req, "listingType", "curated"
        )


def test_verified_drop_schedule():
    param = {"listing_type": "verified"}
    schedule_req = ngw_get_req_with_param("drop_schedule", param)
    # Asserting response status code, response
    Assertions().check_success_status(schedule_req)
    Assertions().assert_response_with_expected_result(
        schedule_req, "message", "Schedule items retrieved"
    )
    Assertions().assert_response_with_expected_result(
        schedule_req, "listingType", "verified"
    )


def test_past_drop_list():
    page = {"current": 1, "size": 10}
    filter_data = {"drop_type": "curated"}
    param = {
        "page": JSONUtil().dump_json(page),
        "filter": JSONUtil().dump_json(filter_data),
    }
    past_drops_req = ngw_get_req_with_param("past_drops", param)
    # Asserting response status code, response
    Assertions().check_success_status(past_drops_req)
    past_drops_result = JSONUtil().find_values_from_json_using_key(
        "results", past_drops_req.text
    )
    assert past_drops_result is not None


def test_recent_drops():
    param = {"upcoming_count": 4, "previous_count": 4}
    recent_drop_req = ngw_get_req_with_param("recent_drops", param)
    # Asserting response status code, response
    Assertions().check_success_status(recent_drop_req)
    open_drop = JSONUtil().find_values_from_json_using_key(
        "openDrop", recent_drop_req.text
    )
    assert open_drop is not None
    previous_drop = JSONUtil().find_values_from_json_using_key(
        "previousDrops", recent_drop_req.text
    )
    assert previous_drop is not None


def test_auction_live():
    live_auction_req = basic_get_req(
        EnvironmentVars.nfgwURL, Endpoint().get_endpoint("live_auctions")
    )
    # Asserting response status code
    Assertions().check_success_status(live_auction_req)


def ngw_get_req_with_param(endpoint, param):
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint(endpoint),
        make_header(
            Constants().headers["content_type"], Constants().headers["app_x_encoded"]
        ),
        param,
    )
    return req
