from conftest import EnvironmentVars

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
token = " OrMTNUUbf3sAmJCdpfuOdCANyxsDGt"
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
