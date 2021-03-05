import json
import requests
import datetime
from KayoAuth import AuthSession, KayoAuthException
from helpers import validate_auth_session
import time




class KayoSession():
    def __init__(self):
        active_profile: object = None
        auth_session: AuthSession = None

    def validate_auth(method):
        def validate_auth_attempts(ref):
            attempts:int = 0
            last_except:Exception = None
            while attempts < 3:
                try:
                    if validate_auth_session(ref.auth_session):
                        break
                    else:
                        raise KayoAuthException

                except Exception as ex:
                        attempts += 1
                        print("Failed to Validate... Attempt {}".format(str(attempts)))
                        last_except = ex
                        time.sleep(1)
            if attempts >= 3:
                print("Out of Attempts")
                raise last_except
            else:
                return method(ref)
        return validate_auth_attempts


    def set_auth_session(self, auth_session):
        self.auth_session = auth_session

    @validate_auth
    def get_profiles(self):
        #Use the Username & Password to make a request to Kayo for your access token       
        requestUrl = "https://profileapi.kayosports.com.au/user/profile"
        requestHeaders={
                "Authorization": "Bearer {}".format(self.auth_session.token),
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
        }

        try:
            print("Contacting Kayo Servers for Profile Details")
            r = requests.request("GET", requestUrl, headers=requestHeaders)
            response_dict = json.loads(r.text)
            print("Profile Fetch Successful")
            return {
                success: True,
                data: response_dict
                }
        except Exception as e:
            print("Response Failed so Something went wrong (Probably your Token)")
            return {
                success: False,
                data: response_dict
                }

    def set_active_profile(self, profile):
        self.active_profile = profile

    
if __name__ == "__main__":
    kayo_auth = AuthSession()
    kayo_session = KayoSession()
    kayo_session.set_auth_session(kayo_auth)
    kayo_auth.import_credentials("../CREDENTIALS.json")
    profiles_response = kayo_session.get_profiles()
    if profiles_response.success:
        kayo_session.set_active_profile(profiles[0])
