from utils.helpers import EnvironmentVars

baseUrl = "https://reqres.in/"

user = {"email": EnvironmentVars.Email, "password": EnvironmentVars.Password}
wrong_user = {"email": "peter@klaven"}

user_Janet = [
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
    "app_json": "application/json",
    "app_x_encoded": "application/x-www-form-urlencoded",
}
