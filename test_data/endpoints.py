class Endpoint:
    def get_endpoint(self, key=None):
        """Returns a dictionary of all endpoints."""
        endpoints = {
            "register": "api/register",
            "user": "api/users/2",
            "login": "api/login",
        }
        if key is None:
            return endpoints
        else:
            return endpoints[key]
