import pytest
import requests

from kapyo.service.kayo_service import KayoService
from tests.unit_tests.constants import *


class TestKayoService:
    def test_default_headers(self,kayo_service,kayo_auth_token):
        headers = kayo_service.default_headers(kayo_auth_token)
        assert headers["Authorization"] == "Bearer "+kayo_auth_token.token

    def test_get_series_events_valid(self,kayo_service,kayo_auth_token,valid_event_response):
        response = kayo_service.get_series_events(kayo_auth_token)
        first_item = response[0]
        assert first_item.id == EVENT_ID
        assert first_item.title == EVENT_TITLE
        assert first_item.description == EVENT_DESCRIPTION
        assert first_item.sport == EVENT_SPORT
        assert first_item.series_id == EVENT_SERIES_ID
        assert first_item.category_id == EVENT_CATEGORY_ID

    def test_get_series_events_invalid(self,kayo_service,kayo_auth_token,failed_response):
        with pytest.raises(Exception):
            response = kayo_service.get_series_events(kayo_auth_token)

    #TODO: Rest of the KayoService Api's



#fixtures
@pytest.fixture
def kayo_service():
    return KayoService()

#mock of requests.Response
class MockResponse:
    text: str = None
    @staticmethod
    def raise_for_status():
        return None


class MockEmptyDictResponse(MockResponse):
    text = f'{{"id":"{PROFILE_ID}"'


class MockFailedResponse(MockResponse):
    @staticmethod
    def raise_for_status():
        raise requests.exceptions.HTTPError


class MockEventsResponse(MockResponse):
    text = f'[{{"id":"{EVENT_ID}","title":"{EVENT_TITLE}",' \
           f'"description":"{EVENT_DESCRIPTION}","sport":"{EVENT_SPORT}",' \
           f'"series_id":{EVENT_SERIES_ID},"category_id":{EVENT_CATEGORY_ID}}}]'

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
def valid_event_response(monkeypatch):
    def mock_request(*args, **kwargs):
        return MockEventsResponse()
    monkeypatch.setattr(requests, "request", mock_request)

