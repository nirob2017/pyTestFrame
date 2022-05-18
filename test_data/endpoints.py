class Endpoint:
    def get_endpoint(self, key=None):
        """Returns a dictionary of all endpoints."""
        endpoints = {
            "register": "api/register",
            "user": "api/users/2",
            "login": "api/login",
            "login_pass": "o/token/",
            "verified_page": "drops/open/?dropType=verified&size=6&current=1",
            "store_page": "builder/get-storefront/?store_url=",
            "wallets": "user/wallet/verified/",
            "stripe_list_card": "stripe/list-cards/",
            "spendable_eth": "user/spendable-eth/",
            "gemini_balance": "user/get-gemini-balance/",
            "gemini_token": "user/is-gemini-token-valid/",
            "complete_purchase": "user/show-completed-purchases/?current=1&size=1",
            "curated_page": "drops/open/?dropType=curated&size=6&current=1",
            "marketplace_page": "marketplace/nifty-types/",
            "collection_page": "builder/get-storefront/",
            "all_minted_nifties": "already_minted_nifties/",
            "search": "https://host-vdgrw7.api.swiftype.com/api/as/v1/engines/nifty-projects/search",
            "nifties_received": "user/show-nifties-received/",
            "nifties_sent": "user/show-nifties-sent/",
            "nifties_deposits": "user/show-deposits/",
            "nifties_withdrawals": "user/show-withdrawals/",
            "profile": "user/profile/",
            "marketplace_project": "marketplace/projects/",
            "popular_nft": "market/ranked-stats/",
            "recent_activity": "market/all-data/",
            "term_condition": "user/accept-terms-and-conditions/",
            "users": "v2/users/",
            "user_verification": "user/verification/",
            "user_update": "user/v2/alter-user-profile/",
            "seller_info": "connect/stripe/info/",
            "email_notification": "user/email/getPreferences/",
            "change_email_notification": "user/email/changePreferences/",
            "price_alert": "user/niftyupdate/get-preferences/",
            "security": "user/twofa/check/",
            "approvals": "user/wallet/eth-contract-approvals/",
            "seller_settings_authorization": "connect/stripe/onboarding-link/",
            "show_received_bids": "user/show-received-bids/",
            "show_placed_bids": "user/show-placed-bids/",
            "show_completed_purchase": "user/show-completed-purchases/",
            "show_successful_sales": "user/show-successful-sales/",
            "all_displays_for_users": "tv/get-all-displays-for-user/",
            "display_nifties": "tv/get-all-display-nifties/",
            "redeem": "redeemable-projects/",
            "redeemable_nifties": "redeemable-projects/nifties/",
            "deposit_nifties": "user/get-deposit-address/",
            "profile_and_nifties": "user/profile-and-nifties/",
            "twofa_preferences": "user/twofa/preferences/",
            "user_nft_search": "v2/users/niftyautomationtestaccount/nifties/",
            "user_external_nifties": "v2/users/niftyautomationtestaccount/external-nifties/",
            "likes_collection": "v2/users/niftyautomationtestaccount/boards/favorites/collections/",
            "likes_nfts": "v2/users/niftyautomationtestaccount/boards/favorites/nifties/",
            "w2w_activity": "payments/historical",
            "past_drops": "market/all-collection-market-stats/",
            "drop_schedule": "drops/schedule/",
            "recent_drops": "home/featured/",
            "live_auctions": "auctions/live/",
            "rates": "v1/fxrates/",
        }
        if key is None:
            return endpoints
        else:
            return endpoints[key]

    def make_contract_address_endpoint(self, contract_address):
        endpoint = f"nifty/metadata-unminted/?contractAddress={contract_address}&niftyType=1&autoReload=false"
        return endpoint

    def make_collection_page_endpoint(self, contract_address):
        endpoint = (
            f"nifty/metadata-unminted/?contractAddress={contract_address}&niftyType=1"
        )
        return endpoint

    def make_marketplace_page_endpoint_contract_address_and_tokenid(
        self, contract_address, token_id
    ):
        endpoint = f"nifty/metadata-minted/?contractAddress={contract_address}&tokenId={token_id}"
        return endpoint
