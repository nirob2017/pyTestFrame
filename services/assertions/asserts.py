from factory.handle_json import JSONUtil


class Assertions:
    def __init__(self):
        super().__init__()

    def check_success_status(self, response):
        assert response.status_code == 200

    def check_response_status_created(self, response):
        assert response.status_code == 201

    def check_bad_Request(self, response):
        assert response.status_code == 400

    def check_unauthorized_response(self, response):
        assert response.status_code == 401

    def check_internal_server_error_response(self, response):
        assert response.status_code == 500

    def check_response(self, response, key=None, value=None):
        req = JSONUtil.load_json(response.text)
        assert req[key] == value

    def assert_response_with_expected_result(
        self, response, response_key=None, expected_data=None, index=0
    ):
        resp = JSONUtil().find_values_from_json_using_key(response_key, response.text)
        assert expected_data == resp[index]
