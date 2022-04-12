import json

from assertpy import assert_that


def check_success_status(self):
    assert self.status_code == 200


def check_bad_Request(self):
    assert self.status_code == 400


def check_response(response, key=None, value=None):
    req = load_json(response.text)
    assert req[key] == value


def assert_id_is_present(is_new_user_created):
    assert_that(is_new_user_created).is_not_empty()


def load_json(json_to_load):
    """Turn json str/bytes into a python object
    :param json_to_load: JSON str/bytes/dict to be loaded into a python object.
    """
    if isinstance(json_to_load, bytes):
        try:
            json_string = json.loads(json_to_load.decode("utf-8"))
        except UnicodeDecodeError:
            json_string = json.loads(json_to_load.decode())
    else:
        json_string = json.loads(json_to_load)
    return json_string
