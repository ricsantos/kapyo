import json
import requests
import datetime
from auth import AuthSession, KayoAuthException
from interface import KayoProfile
from helpers import validate_auth


class KayoSession():
    def __init__(self,active_profile: KayoProfile = None, auth_session: AuthSession = None):
        self.active_profile = active_profile
        self.auth_session= auth_session

    def set_auth_session(self, auth_session):
        self.auth_session = auth_session

    @validate_auth
    def get_profiles(self):
        #Use the Username & Password to make a request to Kayo for your access token       
        request_url = "https://profileapi.kayosports.com.au/user/profile"
        request_headers={
                "Authorization": "Bearer {}".format(self.auth_session.token),
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
        }

        try:
            print("Contacting Kayo Servers for Profile Details")
            r = requests.request("GET", request_url, headers=request_headers)
            response_dict = json.loads(r.text)
            print("Profile Fetch Successful")
            return {
                "success": True,
                "data": response_dict
                }
        except Exception as e:
            print("Response Failed so Something went wrong (Probably your Token)")
            return {
                "success": False
                }

    def set_active_profile(self, profile: object):
        self.active_profile = KayoProfile(profile)

    
if __name__ == "__main__":
    kayo_auth = AuthSession()
    kayo_session = KayoSession()
    kayo_session.set_auth_session(kayo_auth)
    kayo_auth.import_credentials("../TEST_CREDENTIALS.json")
    profiles_response = kayo_session.get_profiles()
    if profiles_response.get("success",False):
        kayo_session.set_active_profile(profiles_response.get("data")[0])
    print(kayo_session.active_profile.id)