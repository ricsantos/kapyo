import json

from kapyo.dataclass.credentials import Credentials

class TestCredentials:
    def test_from_credential_file(self,tmp_credentials_file_object,kayo_auth_username,kayo_auth_password):
        cred = Credentials.from_credential_file(tmp_credentials_file_object)
        assert cred.username == kayo_auth_username
        assert cred.password == kayo_auth_password

    def test_from_login_details(self,kayo_auth_username,kayo_auth_password):
        cred = Credentials.from_login_details(kayo_auth_username,kayo_auth_password)
        assert cred.username == kayo_auth_username
        assert cred.password == kayo_auth_password

    def test_export_credentials_file(self, tmp_credentials_file_path,kayo_auth_json, kayo_auth_credentials):
        cred = kayo_auth_credentials
        cred.export_credentials_file(tmp_credentials_file_path)
        with open(tmp_credentials_file_path,'r') as credentials_file:
            cred_content = json.load(credentials_file)
        assert cred_content == kayo_auth_json
