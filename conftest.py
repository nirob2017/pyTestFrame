import os
from dataclasses import dataclass

import pytest


@dataclass
class EnvironmentVars:
    """Return all secret environment variables"""

    Email = os.getenv("EMAIL")
    Password = os.getenv("PASS")
    BaseURL = os.getenv("Base_Url")
    XmlURL = os.getenv("Xml_Url")
    nfgwURL = os.getenv("NFGW_URL")
    clientID = os.getenv("CLIENT_ID")
    nfgwPass = os.getenv("NFGW_PASS")
    nfgwUser = os.getenv("NFGW_USER")


@pytest.fixture
def invalid_user_data():
    invalid_user = {"emailText": "email", "emailData": "peter@klaven"}
    return invalid_user
