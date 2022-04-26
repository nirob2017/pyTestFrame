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
    "bearer": "Bearer",
    "authentication": "Authorization",
}

error_message_body = "Authentication credentials were not provided."
token = " 54u1Y7Mp1M9sm8CLmHmj93Ef5uDu83"
wallet_address = "0xc0f6080a153fb94b299bc103da13e8b29b59ba02"
