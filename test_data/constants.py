from conftest import EnvironmentVars

user = {"email": EnvironmentVars.Email, "password": EnvironmentVars.Password}

user_janet = [
    {
        "data": {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg",
        },
        "support": {
            "url": "https://reqres.in/#support-heading",
            "text": "To keep ReqRes free, contributions towards server costs are appreciated!",
        },
    }
]

headers = {
    "Accept-Charset": "utf-8",
    "Connection": "keep-alive",
    "content_type": "Content-Type",
    "application_json": "application/json",
    "app_x_encoded": "application/x-www-form-urlencoded",
}

error_message = "Authentication credentials were not provided."
