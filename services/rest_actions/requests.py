from dataclasses import dataclass

import requests


@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:
    """Utility for sending REST api requests."""

    def get(self, url, headers=None):
        """Get request method"""
        response = requests.get(url, headers=headers)
        return self.__get_responses(response)

    def post(self, url, payload=None, headers=None):
        """Post request method. when passing json payload, pass json.dumps(payload)"""
        response = requests.post(url, data=payload, headers=headers)
        return self.__get_responses(response)

    def put(self, url, payload=None, headers=None):
        """Put request method."""
        response = requests.put(url, data=payload, headers=headers)
        return self.__get_responses(response)

    def patch(self, url, payload=None, headers=None):
        """Patch method"""
        response = requests.patch(url, data=payload, headers=headers)
        return self.__get_responses(response)

    def delete(self, url):
        """Delete method."""
        response = requests.delete(url)
        return self.__get_responses(response)

    def __get_responses(self, response):
        status_code = response.status_code
        text = response.text

        try:
            as_dict = response.json()
        except Exception:
            as_dict = {}

        headers = response.headers

        return Response(status_code, text, as_dict, headers)
