import pytest
from assertpy import assert_that

from conftest import EnvironmentVars
from factory.handle_json import JSONUtil
from factory.handle_process import header_with_bearer_token
from services.assertions.asserts import Assertions
from services.rest_actions.requests import APIRequest
from test_data.constants import Constants
from test_data.endpoints import Endpoint
from utils.helpers import nifty_auth_get_request


def test_user_verification():
    resp = nifty_auth_get_request("user_verification")

    # Asserting response status code
    Assertions().check_success_status(resp)


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
    resp = nifty_auth_get_request("seller_info")

    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(
        resp, "stripe_account_id", Constants().stripe_account_id
    )


def test_user_seller_settings_authorization():
    param = {
        "country_code": "CA",
    }

    req = nifty_auth_get_request("seller_settings_authorization", param)

    # Asserting response status code, response
    Assertions().check_success_status(req)
    assert_that([req.as_dict]).extracting("didSucceed").contains(True)


def test_user_email_notification():
    resp = nifty_auth_get_request("email_notification")

    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(
        resp, "message", Constants().notification_options
    )

    __check_and_uncheck_email_notification(Constants().uncheck_all_payload_data, 200)
    __check_and_uncheck_email_notification(Constants().check_all_payload_data, 200)


def test_user_price_alert():
    resp = nifty_auth_get_request("price_alert")

    # Asserting response status code, response
    Assertions().check_success_status(resp)


def test_user_security_check():
    resp = nifty_auth_get_request("security")

    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(resp, "enabled", False)


def test_user_my_account_approval_for_all():
    param = {
        "has_approval_for_all": True,
    }

    req = nifty_auth_get_request("approvals", param)
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
    resp = nifty_auth_get_request("all_displays_for_users")

    # Asserting response status code, response
    Assertions().check_success_status(resp)

    display_nifty_req = nifty_auth_get_request("display_nifties")
    # Asserting response status code, response
    Assertions().check_success_status(display_nifty_req)
    Assertions().assert_response_with_expected_result(
        display_nifty_req, "project_name", Constants().nifty_project_name
    )


def test_user_other_transactions():
    def _sent_post_req(endpoint):
        payload = {"current": 1, "size": 10}
        req = APIRequest().post(
            EnvironmentVars.nfgwURL + Endpoint().get_endpoint()[endpoint],
            payload,
            header_with_bearer_token(),
        )
        return req

    # Received nifties
    received_nft_req = _sent_post_req("nifties_received")
    # Asserting response status code, response
    Assertions().check_success_status(received_nft_req)
    Assertions().assert_response_with_expected_result(
        received_nft_req, "name", "Crystal Pop #3651"
    )

    # Sent nifties
    received_nft_req = _sent_post_req("nifties_sent")
    # Asserting response status code, response
    Assertions().check_success_status(received_nft_req)

    # Deposits nifties
    received_nft_req = _sent_post_req("nifties_deposits")
    # Asserting response status code, response
    Assertions().check_success_status(received_nft_req)

    # Withdrawals nifties
    received_nft_req = _sent_post_req("nifties_withdrawals")
    # Asserting response status code, response
    Assertions().check_success_status(received_nft_req)
    Assertions().assert_response_with_expected_result(
        received_nft_req, "niftyName", "Crystal Pops"
    )


def test_user_deposit_address():
    # Getting user's public deposit address
    resp = nifty_auth_get_request("deposit_nifties")

    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(
        resp, "nifty_public_deposit_address", Constants().public_wallet_address
    )


def test_user_redeem_projects():
    # User's redeemable projects
    resp = nifty_auth_get_request("redeem")

    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(
        resp, "display_name", "Justin Roiland Open Edition"
    )

    # Redeeming project
    payload_data = {"id": 3, "cancelToken": {"promise": {}}, "timeout": 30000}
    req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["redeemable_nifties"],
        payload_data,
        header_with_bearer_token(),
    )
    # Asserting response status code
    Assertions().check_success_status(req)


def test_user_profile_and_nifities_views():
    # User's profile & nifties
    resp = nifty_auth_get_request("profile_and_nifties")

    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(resp, "first_name", "Ash")
    Assertions().assert_response_with_expected_result(
        resp, "project_name", "Crystal Pops 10K"
    )

    # User's profile view preferences
    req = nifty_auth_get_request("twofa_preferences")
    # Asserting response status code, response
    Assertions().check_success_status(resp)
    Assertions().assert_response_with_expected_result(req, "ethereum_withdrawal", False)
    Assertions().assert_response_with_expected_result(req, "login_one_touch", False)


def test_search_user_nft():
    param = {"page": 1, "page_size": 10, "search": 1678, "ordering": ""}

    req = nifty_auth_get_request("user_nft_search", param)
    # Asserting response status code, response
    Assertions().check_success_status(req)
    Assertions().assert_response_with_expected_result(
        req, "name", "Crystal Pop #1678", 1
    )


def test_user_external_nifties():
    param = {
        "page": 1,
        "page_size": 72,
        "walletAddress": Constants().wallet_address,
        "canTrade": True,
        "ordering": "",
    }

    req = nifty_auth_get_request("user_external_nifties", param)
    # Asserting response status code, response
    Assertions().check_success_status(req)
    Assertions().assert_response_with_expected_result(req, "tokenId", "100011547")


def test_user_liked_collection_and_nfts():
    param = {
        "page": 1,
        "page_size": 72,
    }

    collection_req = nifty_auth_get_request("likes_collection", param)
    # Asserting response status code, response
    Assertions().check_success_status(collection_req)

    # User's liked nfts
    nft_req = nifty_auth_get_request("likes_nfts", param)
    # Asserting response status code, response
    Assertions().check_success_status(nft_req)


def test_user_w2w_activity():
    param = {"page": 1, "page_size": 10, "status": "all"}
    # User's wallet to wallet activities
    nft_req = nifty_auth_get_request("w2w_activity", param)
    # Asserting response status code, response
    Assertions().check_success_status(nft_req)


def test_user_profile():
    profile_req = nifty_auth_get_request("profile")
    Assertions().check_success_status(profile_req)

    assert JSONUtil().load_json(profile_req.text) == Constants().profile_data


def __check_and_uncheck_email_notification(data, response):
    change_notification_req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint("change_email_notification"),
        data,
        header_with_bearer_token(),
    )
    # Asserting response status code, response
    assert response == change_notification_req.status_code
