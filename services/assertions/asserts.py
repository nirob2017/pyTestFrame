import json

from assertpy import assert_that


def checkSuccessStatus(self):
    assert self.status_code == 200


def checkBadRequest(self):
    assert self.status_code == 400


def check_response(response, key, value):
    response_content = json.loads(str(response))
    assert response_content[key] == value


def assert_id_is_present(is_new_user_created):
    assert_that(is_new_user_created).is_not_empty()
