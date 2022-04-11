from assertpy import assert_that


def checkSuccessStatus(self):
    assert self.status_code == 200


def checkBadRequest(self):
    assert self.status_code == 400


def assert_people_have_person_with_first_name(response, name):
    assert_that(response.as_dict).extracting("first_name").is_not_empty().contains(name)


def assert_id_is_present(is_new_user_created):
    assert_that(is_new_user_created).is_not_empty()
