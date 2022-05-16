from conftest import EnvironmentVars


class Constants:

    user = {"email": EnvironmentVars.Email, "password": EnvironmentVars.Password}

    user_janet = [
        {
            "data": {
                "id": 2,
                "email": "janet.weaver@reqres.in",
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://reqres.in/img/faces/2-image.jpg",
            },
            "support": {
                "url": "https://reqres.in/#support-heading",
                "text": "To keep ReqRes free, contributions towards server costs are appreciated!",
            },
        }
    ]

    headers = {
        "Accept-Charset": "utf-8",
        "Connection": "keep-alive",
        "content_type": "Content-Type",
        "application_json": "application/json",
        "app_x_encoded": "application/x-www-form-urlencoded",
        "bearer": "Bearer",
        "authentication": "Authorization",
    }

    error_message_body = "Authentication credentials were not provided."
    token = " 7gr9ZcoqndIKP7v3PcbU6rRcf86lAN"
    wallet_address = "0xc0f6080a153fb94b299bc103da13e8b29b59ba02"

    profile_data = {
        "didSucceed": True,
        "errorType": "none",
        "message": "User profile located",
        "userProfile": {
            "account_balance_in_cents": 0,
            "account_balance_holds_in_cents": 0,
            "user_email": "ashiqur.rahman+001@gemini.com",
            "name": "Nifty TestAccount",
            "first_name": "Ash",
            "last_name": "Rah",
            "bio": "None",
            "id": 1006455,
            "profile_pic_url": "https://nftgimagebucket.s3-us-west-1.amazonaws.com/nifty_default_pic1.jpg",
            "profile_url": "niftyautomationtestaccount",
            "verified": False,
            "userGUSDCashoutAddress": "none",
            "userHasGUSDCashoutAddress": False,
            "is_bid_safety_net_exempt": False,
            "userCanCreateNiftyStores": False,
            "twofa_enabled": False,
            "verified_phone_number": False,
            "country_code": "None",
            "phone_number": "None",
            "paymentPreference": "card",
            "max_bid_allowance_override_in_cents": 0,
            "needsTermsAndConditionsApproval": False,
            "user_id": 1009986,
            "verifiedPurchaseEnabled": False,
            "social_links": [],
            "attached_addresses": [
                {
                    "id": 4827183,
                    "uuid": "514c04f2-2382-4748-a1a0-282f070095a7",
                    "address": "0xc0f6080a153fb94b299bc103da13e8b29b59ba02",
                    "is_airdrop_default": True,
                    "can_sync": True,
                }
            ],
            "paymentMethods": {"cards": {}},
        },
    }

    most_popular_nft = "FACES"
    stripe_account_id = "acct_1KxpThR1iodvVx9u"
    notification_options = {
        "purchaseSuccessful": True,
        "purchaseInitiated": True,
        "salesSuccessfulSell": True,
        "salesPlaceForSale": True,
        "storesProfit": True,
        "storesPrimary": True,
        "storesSecondary": True,
        "offersReceive": True,
        "offersMake": True,
        "offersAccept": True,
        "sendNifty": True,
        "receiveNifty": True,
        "cashoutConnectBankAccount": True,
        "cashoutInitiate": True,
        "cashoutComplete": True,
        "projectUpdates": True,
        "storeOpening": True,
        "purchaseOfUnmintedNiftyFails": True,
        "userPlacedBidAccepted": True,
        "depositSuccessful": True,
        "withdrawSucceeded": True,
        "depositFailed": True,
    }

    uncheck_all_payload_data = {"field": "uncheckAll", "pref": False}
    check_all_payload_data = {"field": "checkAll", "pref": True}

    approvals = {"count": 0, "next": None, "previous": None, "results": []}

    bids_purchase_sales_response = {
        "errorType": "none",
        "message": "none",
        "data": {
            "meta": {
                "page": {"total_results": 0, "total_pages": 1, "current": 1, "size": 10}
            },
            "results": [],
        },
        "didSucceed": True,
    }

    nifty_project_name = "Crystal Pops 10K"

    public_wallet_address = "0xe052113bd7d7700d623414a0a4585bcae754e9d5"
