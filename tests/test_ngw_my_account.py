import pytest
from assertpy import assert_that

from conftest import EnvironmentVars
from factory.handle_json import JSONUtil
from factory.handle_process import header_with_bearer_token
from services.assertions.asserts import Assertions
from services.rest_actions.requests import APIRequest
from test_data.constants import Constants
from test_data.endpoints import Endpoint


def test_user_verification():
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("user_verification"),
        header_with_bearer_token(),
    )

    # Asserting response status code
    Assertions().check_success_status(req)


@pytest.mark.skip("Skipping it because we are testing on production env. now.")
@pytest.mark.parametrize(
    "key, value", [("name", "Nifty Test Account"), ("name", "Nifty TestAccount")]
)
def test_update_user_name(key, value):
    payload_data = {
        "bio": "None",
        key: value,
        "profile_url": "niftyautomationtestaccount",
    }
    req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("user_update"),
        payload_data,
        header_with_bearer_token(),
    )

    # Asserting response status code
    Assertions().check_success_status(req)


def test_user_seller_info():
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("seller_info"),
        header_with_bearer_token(),
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)
    Assertions().assert_response_with_expected_result(
        req, "stripe_account_id", Constants().stripe_account_id
    )


def test_user_seller_settings_authorization():
    param = {
        "country_code": "CA",
    }
    req = APIRequest().get(
        EnvironmentVars.nfgwURL
        + Endpoint().get_endpoint("seller_settings_authorization"),
        header_with_bearer_token(),
        param,
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)
    assert_that([req.as_dict]).extracting("didSucceed").contains(True)


def test_user_email_notification():
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("email_notification"),
        header_with_bearer_token(),
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)
    Assertions().assert_response_with_expected_result(
        req, "message", Constants().notification_options
    )

    _check_and_uncheck_email_notification(Constants().uncheck_all_payload_data, 200)
    _check_and_uncheck_email_notification(Constants().check_all_payload_data, 200)


def test_user_price_alert():
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("price_alert"),
        header_with_bearer_token(),
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)


def test_user_security_check():
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("security"),
        header_with_bearer_token(),
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)
    Assertions().assert_response_with_expected_result(req, "enabled", False)


def test_user_my_account_approval_for_all():
    param = {
        "has_approval_for_all": True,
    }
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("approvals"),
        header_with_bearer_token(),
        param,
    )
    # Asserting response status code, response
    Assertions().check_success_status(req)
    Assertions().assert_response_with_expected_result(
        req, "approvals", Constants().approvals
    )


@pytest.mark.parametrize(
    "endpoint, response",
    [
        ("show_received_bids", Constants().bids_purchase_sales_response),
        ("show_placed_bids", Constants().bids_purchase_sales_response),
        ("show_completed_purchase", Constants().bids_purchase_sales_response),
        ("show_successful_sales", Constants().bids_purchase_sales_response),
    ],
)
def test_user_show_received_placed_bids_and_completed_purchase_sales(
    endpoint, response
):
    payload_data = {"current": 1, "size": 10}
    req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint(endpoint),
        payload_data,
        header_with_bearer_token(),
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)
    assert JSONUtil().load_json(req.text) == response


def test_user_displays_nifties():
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("all_displays_for_users"),
        header_with_bearer_token(),
    )

    # Asserting response status code, response
    Assertions().check_success_status(req)

    display_nifty_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("display_nifties"),
        header_with_bearer_token(),
    )
    # Asserting response status code, response
    Assertions().check_success_status(display_nifty_req)
    Assertions().assert_response_with_expected_result(
        display_nifty_req, "project_name", Constants().nifty_project_name
    )


def _check_and_uncheck_email_notification(data, response):
    change_notification_req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("change_email_notification"),
        data,
        header_with_bearer_token(),
    )
    # Asserting response status code, response
    assert response == change_notification_req.status_code
