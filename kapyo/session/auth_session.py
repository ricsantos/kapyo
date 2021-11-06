from kapyo.service.auth_service import AuthService, KayoAuthService
from kapyo.dataclass.token import KayoAuthToken
from kapyo.dataclass.credentials import Credentials
from kapyo.helpers import retry

import logging


class AuthSession:
    def __init__(self,auth_service=None):
        self.auth_token: KayoAuthToken = None
        self.auth_service: AuthService
        self._cached_credentials: Credentials = None

        self._setup_service(auth_service)

    def _setup_service(self,service):
        if service:
            self.auth_service = service
        else:
            self.auth_service = KayoAuthService()

    @property
    def session_expired(self) -> bool:
        if self.auth_token is not None:
            return self.auth_token.is_token_expired
        else:
            return True

    def set_login_details(self, username: str, password: str):
        cred = Credentials.from_login_details(username, password)
        self._cached_credentials = cred

    def set_credentials_path(self, path):
        cred = Credentials.from_credential_file(path)
        self._cached_credentials = cred

    def connect(self):
        # Try to use current token if it exists
        if self.auth_token is not None:
            try:
                self.auth_token = self._refresh()
                logging.info("Refreshed Authentication Token")
            except Exception as ex:
                logging.error(ex)
                raise ex
        else:
            # Try to use cached credentials if they exist
            if self._cached_credentials:
                try:
                    self.auth_token = self._login(self._cached_credentials)
                    logging.info("Logged in to Authentication Service with Cached Credentials")
                except Exception as ex:
                    logging.error(ex)
                    raise ex

    @retry
    def _login(self, credentials: Credentials) -> KayoAuthToken:
        # When session needs to get a new authentication token
        return self.auth_service.login(credentials)

    @retry
    def _refresh(self) -> KayoAuthToken:
        # when a session needs to refresh the current token
        return self.auth_service.refresh_token(self.auth_token)
