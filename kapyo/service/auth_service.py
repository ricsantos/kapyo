import requests
from abc import ABC, abstractmethod
import datetime
import json
import logging

from kapyo.dataclass.token import KayoAuthToken
from kapyo.dataclass.credentials import Credentials

class KayoAuthException(Exception):
    """Raised When the Authentication Session Failed to Handle Login Attempt"""
    def __init__(self, message="The Authentication Service failed to Login"):
        self.message = message
        super().__init__(self.message)

class AuthService(ABC):
    @abstractmethod
    def login(self) -> KayoAuthToken:
        pass

    @abstractmethod
    def refresh_token(self) -> KayoAuthToken:
        pass

class KayoAuthService(AuthService):
    # Auth0 Tenant client ID used by Kayo
    CLIENTID = "qjmv9ZvaMDS9jGvHOxVfImLgQ3G5NrT2"
    OAUTH_URL = "https://auth.kayosports.com.au"
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
    }

    def _generate_token(self,r: requests.Response,refresh_token: str = None) -> KayoAuthToken:
        r.raise_for_status()
        response_dict = json.loads(r.text)
        if (response_dict.get("access_token", None) is None):
            raise KayoAuthException
        else:
            auth_token = KayoAuthToken(
                token=response_dict["access_token"],
                token_expires_in=response_dict["expires_in"],
                refresh_token=response_dict["refresh_token"] if refresh_token is None else refresh_token,
                token_created_at=datetime.datetime.now()
            )
            print("Login Successful")
            return auth_token

    def login(self, credentials: Credentials) -> KayoAuthToken:
        """Use the Credentials to make a request to Kayo for an access token"""
        request_url = self.OAUTH_URL + "/oauth/token"
        request_json = "{\n" + \
                       " \"audience\":\"kayosports.com.au\",\n" + \
                       "\"grant_type\":\"http://auth0.com/oauth/grant-type/password-realm\",\n" + \
                       "\"scope\": \"openid offline_access\", \n" + \
                       "\"realm\": \"prod-martian-database\",\n" + \
                       "\"client_id\": \"" + self.CLIENTID + "\",\n" + \
                       "\"username\": \"" + credentials.username + "\",\n" + \
                       "\"password\": \"" + credentials.password + "\"\n}"
        try:
            print("Contacting Kayo Servers with Login Details")
            r = requests.request("POST", request_url, data=request_json, headers=self.DEFAULT_HEADERS)
            return self._generate_token(r)
        except Exception as ex:
            logging.exception("Exception While Logging in to Authentication Service")
            raise ex

    def refresh_token(self, auth_token: KayoAuthToken) -> KayoAuthToken:
        """Refresh the Authentication token"""
        request_url = self.OAUTH_URL + "/oauth/token"
        request_json = "{\n" + \
                   " \"redirectUri\":\"https://kayosports.com.au/login\",\n" + \
                   "\"client_id\": \"" + self.CLIENTID + "\",\n" + \
                   "\"grant_type\":\"refresh_token\",\n" + \
                   "\"refresh_token\": \"" + auth_token.refresh_token + "\" \n}"
        try:
            print("Contacting Kayo Servers with Refresh Token")
            r = requests.request("POST", request_url, data=request_json, headers=self.DEFAULT_HEADERS)
            return self._generate_token(r, auth_token.refresh_token)
        except Exception as ex:
            logging.exception("Exception While Refreshing Token in Authentication Service")
            raise ex
