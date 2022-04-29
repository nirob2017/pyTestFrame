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
            "profile": "user/profile/",
            "marketplace_project": "marketplace/projects/",
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
