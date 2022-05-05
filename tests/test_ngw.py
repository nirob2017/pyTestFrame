import pytest
from conftest import EnvironmentVars
from factory.handle_json import JSONUtil
from factory.handle_process import make_header, basic_get_req
from services.assertions.asserts import Assertions
from services.rest_actions.requests import APIRequest
from test_data.constants import (
    headers,
    error_message_body,
    token,
    wallet_address,
    profile_data,
    most_popular_nft,
)
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

    # Checking Terms and condition API
    accept_term_and_condition = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["term_condition"],
        "",
        make_header(headers["authentication"], headers["bearer"] + token),
    )
    Assertions().check_success_status(accept_term_and_condition)


@pytest.mark.skip()
def test_select_nft_from_marketplace():
    """
    Test for visiting marketplace page, then collection page, after that selecting and NFT &
    making a purchase of an NFT using bearer token
    """

    params = {
        "page": {"current": 1, "size": 1},
        "filter": {"currently_on_sale": True, "listing_type": ["curated"]},
    }

    market_page_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["marketplace_page"],
        make_header(headers["content_type"], headers["app_x_encoded"]),
        JSONUtil().dump_json(params),
    )

    # Processing Json Response
    result = JSONUtil().load_json(market_page_req.text)

    # Retrieving collection page address from json data
    collection_page_address = result["data"]["results"][0]["niftyContractAddress"]
    print(collection_page_address)
    Assertions().check_success_status(market_page_req)

    # Visiting collection page
    collection_page_req = basic_get_req(
        EnvironmentVars.nfgwURL,
        Endpoint().make_collection_page_endpoint(collection_page_address),
    )
    Assertions().check_success_status(collection_page_req)

    params_for_nft_collection = {
        "page": {"current": 1, "size": 52},
        "filter": {
            "currently_on_sale": True,
            "nifty_type_that_created": "1",
            "contract_address": collection_page_address,
        },
        "sort": {"price_in_cents": "asc"},
    }

    listed_nft_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["all_minted_nifties"],
        make_header(headers["content_type"], headers["app_x_encoded"]),
        JSONUtil().dump_json(params_for_nft_collection),
    )

    print(listed_nft_req)


def test_show_received_nft():
    payload = {"current": 1, "size": 10}
    received_nft_req = APIRequest().post(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["nifties_received"],
        payload,
        make_header(headers["authentication"], headers["bearer"] + token),
    )
    Assertions().check_success_status(received_nft_req)

    # Processing Json Response
    process_nft_res = JSONUtil().load_json(received_nft_req.text)

    # Retrieving first NFT name from json data
    data = JSONUtil().find_values_from_json_using_key("name", received_nft_req.text)
    assert data[0] == "Crystal Pop #3651"


def test_user_profile():
    profile_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["profile"],
        make_header(headers["authentication"], headers["bearer"] + token),
    )
    Assertions().check_success_status(profile_req)

    assert JSONUtil().load_json(profile_req.text) == profile_data


def test_select_curated_nft_from_marketplace():
    """
    Test for visiting marketplace page, then collection page, after that selecting and NFT &
    making a purchase of an NFT using bearer token
    """

    params = 'page={"current":1,"size":1}&filter={"listing_type":"curated"}'

    market_page_curated_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["marketplace_project"],
        make_header(headers["content_type"], headers["app_x_encoded"]),
        params,
    )

    # Processing Json Response
    result = JSONUtil().load_json(market_page_curated_req.text)

    # Retrieving collection page address from json data
    store_contract_address = JSONUtil().find_values_from_json_using_key(
        "contractAddress", market_page_curated_req.text
    )
    print(store_contract_address)

    store_params = (
        'page={"current":1,"size":52}&filter={"listing_type":[],'
        '"contractAddress":"0x38cb271642fbd19a2592a15504420b1a78288a62"} '
    )

    # Visiting NFT store collection page
    collection_page_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["marketplace_page"],
        make_header(headers["content_type"], headers["app_x_encoded"]),
        store_params,
    )
    Assertions().check_success_status(collection_page_req)

    # Finding first NFT contract address
    nft_contract_address = JSONUtil().find_values_from_json_using_key(
        "niftyContractAddress", collection_page_req.text
    )

    # Visiting first NFT page
    store_page_req = basic_get_req(
        EnvironmentVars.nfgwURL,
        Endpoint().make_collection_page_endpoint(nft_contract_address[0]),
    )
    Assertions().check_success_status(store_page_req)


def test_most_popular_nft():
    """
    Test for hitting most popular NFTs endpoint, then selecting an NFT & asserting it
    """

    param = {
        "size": 2,
        "current": 1,
        "ranking_type": "number_of_sm_sales",
        "order_by": "asc",
    }

    most_popular_nft_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["popular_nft"],
        make_header(headers["content_type"], headers["app_x_encoded"]),
        param,
    )
    Assertions().check_success_status(most_popular_nft_req)

    # Finding all contract address from json response
    nft_contract_address = JSONUtil().find_values_from_json_using_key(
        "contractAddress", most_popular_nft_req.text
    )

    # Visiting first popular nft page using contract address
    popular_nft_page_req = APIRequest().get(
        EnvironmentVars.nfgwURL
        + Endpoint().make_contract_address_endpoint(nft_contract_address[0]),
        make_header(headers["content_type"], headers["app_x_encoded"]),
    )
    Assertions().check_success_status(popular_nft_page_req)

    # Finding NFT title from json response
    nft_title = JSONUtil().find_values_from_json_using_key(
        "niftyTitle", popular_nft_page_req.text
    )
    assert nft_title[0] == most_popular_nft


def test_recent_activity():
    """
    Test for hitting recent activity endpoint, then selecting first activity & asserting it
    """

    param = {
        "size": 20,
        "current": 1,
        "order_by": "asc",
        "onlySales": True,
        "includeProfiles": False,
    }
    recent_activity_req = APIRequest().get(
        EnvironmentVars.nfgwURL + Endpoint().get_endpoint()["recent_activity"],
        make_header(headers["content_type"], headers["app_x_encoded"]),
        param,
    )
    Assertions().check_success_status(recent_activity_req)

    # Finding all contract address from json response
    nft_contract_address = JSONUtil().find_values_from_json_using_key(
        "contractAddress", recent_activity_req.text
    )

    # Finding all token id from json response
    token_id = JSONUtil().find_values_from_json_using_key(
        "tokenId", recent_activity_req.text
    )

    # Visiting NFT page using contract address & token id
    nft_page_req = APIRequest().get(
        EnvironmentVars.nfgwURL
        + Endpoint().make_marketplace_page_endpoint_contract_address_and_tokenid(
            nft_contract_address[0], token_id[0]
        ),
        make_header(headers["content_type"], headers["app_x_encoded"]),
    )
    Assertions().check_success_status(nft_page_req)


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


def authentication_error_assertions_of_api(endpoint):
    req = basic_get_req(EnvironmentVars.nfgwURL, Endpoint().get_endpoint()[endpoint])
    req_data = JSONUtil().load_json(req.text)
    assert req_data["detail"] == error_message_body
    Assertions().check_unauthorized_response(req)
