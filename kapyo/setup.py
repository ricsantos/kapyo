from .auth import AuthSession
from .session import KayoSession


def setup(credentials_path):
    #Create an Authentication Session using the Credentials path
    auth_session = AuthSession(credentials_path =credentials_path)
    kayo_session= KayoSession(auth_session=auth_session)
    kayo_session.get_profiles
    profiles_response = kayo_session.get_profiles()
    if profiles_response.get("success",False):
        kayo_session.set_active_profile(profiles_response.get("data")[0])
    return kayo_session


def create_empty_credentials_file(credentials_path):
        try:
            credentials_json = {
                "USERNAME":"yourkayoemail@domain.com",
                "PASSWORD":"Y0urP@s5w0rd"
            }
            with open(credentials_path, 'w+') as credentials_file:
                json.dump(credentials_json, credentials_file)
        except:
            "Something went wrong with creating the credentials file"

def create_credentials_file(username, password):
    try:
        credentials_json = {
                "USERNAME":username,
                "PASSWORD":password
        }
        with open(credentials_path, 'w+') as credentials_file:
            json.dump(credentials_json, credentials_file)
    except:
            "Something went wrong with creating the credentials file"