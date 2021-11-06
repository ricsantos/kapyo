import pytest
import requests
from kapyo.service.auth_service import KayoAuthService, KayoAuthException

from tests.unit_tests.constants import TOKEN,TOKEN_EXPIRES_IN,REFRESH_TOKEN


class TestKayoAuthService:
    def test_login_valid(self,valid_login_response,kayo_auth_service,kayo_auth_credentials,constants):
        auth_token = kayo_auth_service.login(kayo_auth_credentials)
        assert auth_token.token == constants["TOKEN"]
        assert auth_token.refresh_token == constants["REFRESH_TOKEN"]
        assert auth_token.token_expires_in == 300

    def test_login_empty(self,empty_response,kayo_auth_service,kayo_auth_credentials):
        with pytest.raises(KayoAuthException):
            auth_token = kayo_auth_service.login(kayo_auth_credentials)

    def test_login_fail(self,failed_response,kayo_auth_service,kayo_auth_credentials):
        with pytest.raises(Exception):
            auth_token = kayo_auth_service.login(kayo_auth_credentials)

    def test_refresh_token_valid(self,valid_refresh_response,kayo_auth_service,kayo_auth_token,constants):
        auth_token = kayo_auth_service.refresh_token(kayo_auth_token)
        assert auth_token.token == constants["TOKEN"]
        assert auth_token.refresh_token == constants["REFRESH_TOKEN"]
        assert auth_token.token_expires_in == 300

    def test_refresh_token_empty(self,empty_response,kayo_auth_service,kayo_auth_token):
        with pytest.raises(KayoAuthException):
            auth_token = kayo_auth_service.refresh_token(kayo_auth_token)

    def test_refresh_token_fail(self,failed_response,kayo_auth_service,kayo_auth_token):
        with pytest.raises(Exception):
            auth_token = kayo_auth_service.refresh_token(kayo_auth_token)



@pytest.fixture
def kayo_auth_service():
    return KayoAuthService()


#mock of requests.Response
class MockResponse:
    text: str = None
    @staticmethod
    def raise_for_status():
        return None


class MockEmptyDictResponse(MockResponse):
    text = "{}"


class MockFailedResponse(MockResponse):
    @staticmethod
    def raise_for_status():
        raise requests.exceptions.HTTPError


class MockLoginResponse(MockResponse):
    text = f'{{"access_token":"{TOKEN}","expires_in":{TOKEN_EXPIRES_IN},"refresh_token":"{REFRESH_TOKEN}"}}'


class MockRefreshResponse(MockResponse):
    text = f'{{"access_token":"{TOKEN}","expires_in":{TOKEN_EXPIRES_IN}}}'


@pytest.fixture()
def empty_response(monkeypatch):
    def mock_request(*args, **kwargs):
        return MockEmptyDictResponse()
    monkeypatch.setattr(requests, "request", mock_request)

@pytest.fixture()
def failed_response(monkeypatch):
    def mock_request(*args, **kwargs):
        return MockFailedResponse()
    monkeypatch.setattr(requests, "request", mock_request)

@pytest.fixture()
def valid_login_response(monkeypatch):
    def mock_request(*args, **kwargs):
        return MockLoginResponse()
    monkeypatch.setattr(requests, "request", mock_request)

@pytest.fixture()
def valid_refresh_response(monkeypatch):
    def mock_request(*args, **kwargs):
        return MockRefreshResponse()
    monkeypatch.setattr(requests, "request", mock_request)





