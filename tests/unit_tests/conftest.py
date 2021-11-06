import pytest
import pathlib
import json
import datetime

from kapyo.dataclass.credentials import Credentials
from kapyo.service.auth_service import KayoAuthToken
from tests.unit_tests.constants import USERNAME,PASSWORD,TOKEN,REFRESH_TOKEN,TOKEN_EXPIRES_IN

@pytest.fixture(scope="session", autouse=True)
def constants():
    return {
        "USERNAME": USERNAME,
        "PASSWORD": PASSWORD,
        "TOKEN": TOKEN,
        "REFRESH_TOKEN": REFRESH_TOKEN,
        "TOKEN_EXPIRES_IN": TOKEN_EXPIRES_IN
    }

@pytest.fixture
def kayo_auth_username(constants):
    return constants["USERNAME"]

@pytest.fixture
def kayo_auth_password(constants):
    return constants["PASSWORD"]

@pytest.fixture
def kayo_auth_json(kayo_auth_username,kayo_auth_password):
    return {
        "USERNAME": kayo_auth_username,
        "PASSWORD": kayo_auth_password
    }

@pytest.fixture
def kayo_auth_credentials(kayo_auth_username,kayo_auth_password) -> Credentials:
    return Credentials(username=kayo_auth_username,password=kayo_auth_password)


@pytest.fixture
def tmp_credentials_file_path(tmp_path:pathlib.Path) -> pathlib.Path:
    file = tmp_path / "CREDENTIALS.json"
    return file

@pytest.fixture
def tmp_credentials_file_object(tmp_credentials_file_path: pathlib.Path, kayo_auth_json: dict) -> pathlib.Path:
    with open(tmp_credentials_file_path, 'w+') as credentials_file:
        json.dump(kayo_auth_json, credentials_file)
    return tmp_credentials_file_path


@pytest.fixture
def kayo_auth_token(constants):
    token = KayoAuthToken(
        token=constants["TOKEN"],
        token_expires_in=constants["TOKEN_EXPIRES_IN"],
        refresh_token=constants["REFRESH_TOKEN"],
        token_created_at=datetime.datetime.now()
    )
    return token
