from kapyo.session.auth_session import AuthSession
from kapyo.dataclass.profile import KayoProfile
from kapyo.service.kayo_service import KayoService
from kapyo.helpers import authenticate


class KayoSession:
    def __init__(self, auth_session: AuthSession = None, kayo_service: KayoService = None):
        self.active_profile: KayoProfile
        self.auth_session: AuthSession
        self.kayo_service: KayoService

        self._setup_service(kayo_service)
        self._setup_auth_session(auth_session)

    def _setup_service(self, service):
        if service:
            self.kayo_service = service
        else:
            self.kayo_service = KayoService()

    def _setup_auth_session(self,session):
        if session:
            self.auth_session = session
        else:
            self.auth_session = AuthSession()

    def token(self):
        if self.auth_session.auth_token is None:
            self.auth_session.connect()
        return self.auth_session.auth_token

    def login(self, username,password):
        self.auth_session.set_login_details(username,password)
        self.auth_session.connect()

    def credentials(self,path):
        self.auth_session.set_credentials_path(path)
        self.auth_session.connect()


    @authenticate
    def get_profiles(self):
        return self.kayo_service.get_profiles()

    @authenticate
    def get_profile_events(self):
        return self.kayo_service.get_profile_events()

    @authenticate
    def get_series_events(self,sport,series,token):
        return self.kayo_service.get_series_events(token, sport, series)

    @authenticate
    def get_stream_manifests(self,stream_id, recommended,format_filter):
        return self.kayo_service.get_stream_manifests(stream_id, recommended, format_filter)

