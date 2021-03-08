import time
import requests
from .auth import AuthSession, KayoAuthException

"""
Helper Function used to Handle the Authorisation Flow
Login if Necessary or Use the established Refresh token to update the Bearer Token

Returns True if the Session is Validated or False if something went wrong and the auth session should not be used in requests
"""
def validate_auth_session(auth_session):
    if not isinstance(auth_session,AuthSession):
        #The passed variable is not an auth session
        raise TypeError
    #Check if logged in
    if auth_session.token is not None:
        #Check if the tokens has expired
        if auth_session.is_token_expired():
            print('Token expired... Resetting')
            if auth_session.reset_token():
                print('Token Reset')
            else:
                return False
    else:
        print('No Token. Logging in...')
        if auth_session.login():
            print('Logged In')
        else:
            return False

    return True


"""
Decorator for Methods used to ensure the reference instance has a valid auth_session variable
before it is used to make kayo api requests

Usage:
@validate_auth
def example_method(self):
    request_url = "someKayoUrl"
    request_headers = {
        "Authorization": "Bearer {}".format(self.auth_session.token),
    } 
    response = requests.request("GET", request_url, headers=request_headers)
    return response
"""
def validate_auth(method):
    def validate_auth_attempts(ref, *args, **kwargs):
        #Attempt to validate the Authorisation session 
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
            return method(ref, *args, **kwargs)
    return validate_auth_attempts


"""
Check if the Stream Link provides a Manifest that is accessible
"""
def validate_stream_link(stream_link):
        try:
            request_url = stream_link
            r = requests.request("GET", request_url)
            if str(r.status_code) == '200':
                return True
            else:
                return False
        except:
            return False
        