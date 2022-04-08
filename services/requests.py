from dataclasses import dataclass

import requests


@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:
    def postReqWithoutHeader(url, payload=None):
        response = requests.post(url, json=payload)
        return response

    def get(url):
        response = requests.get(url)
        return response

    def post(self, url, payload=None, headers=None):
        response = requests.post(url, data=payload, headers=headers)
        return self.__get_responses(response)

    def delete(self, url):
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
