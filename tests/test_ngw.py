import pytest

from conftest import EnvironmentVars
from factory.handle_json import JSONUtil
from factory.handle_process import make_header, basic_get_req
from services.assertions.asserts import Assertions
from services.rest_actions.requests import APIRequest
from test_data.constants import headers, error_message_body, token, wallet_address
from test_data.endpoints import Endpoint


@pytest.mark.xfail
def test_login_with_two_fa():
    data = {
        "grant_type": "password",
        "client_id": EnvironmentVars.clientID,
        "password": EnvironmentVars.nfgwPass,
        "username": EnvironmentVars.nfgwUser,
        "captcha_token_v3": "captchaTokenV3",
    }
    req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["login_pass"],
        data,
        make_header(headers["content_type"], headers["app_x_encoded"]),
    )


@pytest.mark.skip("Refresh token works only once")
def test_login_with_refresh_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": EnvironmentVars.clientID,
        "refresh_token": "refresh_token",
    }

    req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["login_pass"],
        data,
        make_header(headers["content_type"], headers["app_x_encoded"]),
    )
    Assertions().check_success_status(req)
    print(req.text)


def test_purchase_verified_nft_without_login():
    """
    Test for visiting verified NFT page, then store NFT & making a purchase of an NFT
    """

    # Visiting Verified NFT collection page
    verified_page_req = basic_get_req(
        EnvironmentVars.nfgwURL, Endpoint().get_endpoint()["verified_page"]
    )

    # Processing Json Response
    data = JSONUtil().load_json(verified_page_req.text)

    # Retrieving store name from json data
    store_name = JSONUtil().get_value_list_by_node_name("storeURL", data)
    print(store_name[0])
    Assertions().check_success_status(verified_page_req)

    # Visiting First NFT Store page
    store_req = basic_get_req(
        EnvironmentVars.nfgwURL,
        Endpoint().get_endpoint()["store_page"] + store_name[0],
    )

    # Processing Json Response
    process_store = JSONUtil().load_json(store_req.text)

    # Retrieving first NFT from store of json data
    contract_address = JSONUtil().get_value_list_by_node_name(
        "contractAddress", process_store
    )
    print(contract_address[0])
    Assertions().check_success_status(store_req)

    # Visiting First NFT page
    nft_req = basic_get_req(
        EnvironmentVars.nfgwURL,
        Endpoint().make_contract_address_endpoint(contract_address[0]),
    )
    Assertions().check_success_status(nft_req)

    # Checking user wallets
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["wallets"]
    )
    Assertions().check_unauthorized_response(req)

    # Requesting to different APIs endpoints & checking responses, status codes
    authentication_error_assertions_of_api("stripe_list_card")
    authentication_error_assertions_of_api("gemini_balance")
    authentication_error_assertions_of_api("spendable_eth")
    authentication_error_assertions_of_api("gemini_token")
    authentication_error_assertions_of_api("complete_purchase")


def authentication_error_assertions_of_api(endpoint):
    req = basic_get_req(EnvironmentVars.nfgwURL, Endpoint().get_endpoint()[endpoint])
    req_data = JSONUtil().load_json(req.text)
    assert req_data["detail"] == error_message_body
    Assertions().check_unauthorized_response(req)


def test_purchase_curated_nft_with_login():
    """
    Test for visiting curated NFT page, then store NFT & making a purchase of an NFT using bearer token
    """

    # Visiting Verified NFT collection page
    collection_page_req = basic_get_req(
        EnvironmentVars.nfgwURL, Endpoint().get_endpoint()["curated_page"]
    )

    # Processing Json Response
    data = JSONUtil().load_json(collection_page_req.text)

    # Retrieving store name from json data
    store_name = JSONUtil().get_value_list_by_node_name("storeURL", data)
    print(store_name[3])
    Assertions().check_success_status(collection_page_req)

    # Visiting First NFT Store page
    store_req = basic_get_req(
        EnvironmentVars.nfgwURL,
        Endpoint().get_endpoint()["store_page"] + store_name[3],
    )

    # Processing Json Response
    process_store = JSONUtil().load_json(store_req.text)

    # Retrieving first NFT from store of json data
    contract_address = JSONUtil().get_value_list_by_node_name(
        "contractAddress", process_store
    )
    print(contract_address)
    Assertions().check_success_status(store_req)

    # Visiting First NFT page
    nft_req = basic_get_req(
        EnvironmentVars.nfgwURL,
        Endpoint().make_contract_address_endpoint(contract_address[0]),
    )
    Assertions().check_success_status(nft_req)

    # Checking user wallets
    wallet_address_from_response = authentication_success_assertion_of_api(
        "wallets", "address"
    )
    assert wallet_address_from_response[0] == wallet_address
    authentication_success_assertion_of_api("stripe_list_card", "data")

    # Checking ethereum wallet
    eth_response = authentication_success_assertion_of_api(
        "spendable_eth", "max_withdrawal_balance"
    )
    assert eth_response[0]["eth"] == 0

    # Checking Gemini balance API
    gemini_balance_response = make_get_request_with_token("gemini_balance")
    Assertions().check_bad_Request(gemini_balance_response)

    # Checking Gemini token API
    gemini_token_response = make_get_request_with_token("gemini_token")
    Assertions().check_internal_server_error_response(gemini_token_response)

    # Checking Complete purchase API
    purchase_response = make_get_request_with_token("complete_purchase")
    Assertions().check_success_status(purchase_response)


def make_get_request_with_token(endpoint):
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()[endpoint],
        make_header(headers["authentication"], headers["bearer"] + token),
    )
    return req


def authentication_success_assertion_of_api(endpoint, key=None):
    req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()[endpoint],
        make_header(headers["authentication"], headers["bearer"] + token),
    )

    # Asserting response status code
    Assertions().check_success_status(req)

    # Searching a key in json response returning it as array
    req = JSONUtil().load_json(req.text)
    response_array = JSONUtil().get_value_list_by_node_name(key, req)
    return response_array
