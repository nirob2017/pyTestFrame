from factory.handle_json import JSONUtil


class Assertions:
    @staticmethod
    def check_success_status(response):
        assert response.status_code == 200

    @staticmethod
    def check_response_status_created(response):
        assert response.status_code == 201

    @staticmethod
    def check_bad_Request(response):
        assert response.status_code == 400

    @staticmethod
    def check_unauthorized_response(response):
        assert response.status_code == 401

    @staticmethod
    def check_internal_server_error_response(response):
        assert response.status_code == 500

    @staticmethod
    def check_response(response, key=None, value=None):
        req = JSONUtil.load_json(response.text)
        assert req[key] == value

    @staticmethod
    def assert_response_with_expected_result(
        response, response_key=None, expected_data=None
    ):
        resp = JSONUtil().find_values_from_json_using_key(response_key, response.text)
        assert expected_data == resp[0]
