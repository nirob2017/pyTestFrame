import pytest

from conftest import EnvironmentVars
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


def _check_and_uncheck_email_notification(data, response):
    change_notification_req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("change_email_notification"),
        data,
        header_with_bearer_token(),
    )
    # Asserting response status code, response
    assert response == change_notification_req.status_code
