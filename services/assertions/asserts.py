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
    def check_response(response, key=None, value=None):
        req = JSONUtil.load_json(response.text)
        assert req[key] == value
