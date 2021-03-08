import json
import requests
import datetime
from .auth import AuthSession, KayoAuthException
from .interface import KayoProfile, KayoStreamLink
from .helpers import validate_auth, validate_stream_link


class KayoSession():
    def __init__(self,active_profile: KayoProfile = None, auth_session: AuthSession = None):
        self.active_profile = active_profile
        self.auth_session= auth_session

    def set_auth_session(self, auth_session):
        self.auth_session = auth_session

    def set_active_profile(self, profile: object):
        self.active_profile = KayoProfile(profile)
    
    """
    Ask Kayo for the Profiles associated with the Account
    """
    @validate_auth
    def get_profiles(self):       
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

    """
    Ask Kayo for the personalised Events it thinks this Profile is interested in
    """
    @validate_auth
    def get_profile_events(self, evaluate: int = None, profile: str = None):
        #if no profile Id is provided use the active profile from the current session if it exists
        if (profile is None) and (self.active_profile is not None):
            profile = self.active_profile.id

        #Use the Username & Password to make a request to Kayo for your access token       
        request_url = "https://vccapi.kayosports.com.au/v2/content/types/landing/names/sports"
        request_headers={
                "Authorization": "Bearer {}".format(self.auth_session.token),
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
        }
        request_params = dict()
        if evaluate is not None:
            request_params['evaluate'] = evaluate
        if profile is not None:
            request_params['profile'] = profile

        try:
            r = requests.request("GET", request_url, params = request_params, headers = request_headers)
            if str(r.status_code) != '200':
                raise Exception('Status: '+r.status_code+ ' trying to access '+ request_url)
            else:
                response_dict = json.loads(r.text)
                print("Series Event Successful")
                return {
                    "success": True,
                    "data": response_dict
                    }
        except Exception as e:
            print(e.message)
            return {
                "success": False

                }

    """
    Ask Kayo for the Events for a given Sport and or Series
    """
    @validate_auth
    def get_series_events(self, evaluate: int = None, sport: str = None, series: str = None):
         #Use the Username & Password to make a request to Kayo for your access token       
        request_url = "https://vccapi.kayosports.com.au/v2/content/types/landing/names/series"
        request_headers={
                "Authorization": "Bearer {}".format(self.auth_session.token),
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
        }

        #Provide the Parameters if they exist
        request_params = dict()
        if evaluate is not None:
            request_params['evaluate'] = evaluate
        if sport is not None:
            request_params['sport'] = sport
        if series is not None:
            request_params['series'] = series
        
        try:
            r = requests.request("GET", request_url, params = request_params, headers = request_headers)
            if str(r.status_code) != '200':
                raise Exception('Status: '+r.status_code+ ' trying to access '+ request_url)
            else:
                response_dict = json.loads(r.text)
                print("Series Event Successful")
                return {
                    "success": True,
                    "data": response_dict
                    }
        except Exception as e:
            print(e.message)
            return {
                "success": False
                }

    @validate_auth
    def get_stream_links(self, stream_id, recommended=False, validate_links = True, format_filter= None):
         #Use the Username & Password to make a request to Kayo for your access token       
        request_url = "https://vmndplay.kayosports.com.au/api/v1/asset/{stream_id}/play?fields=alternativeStreams".format(stream_id = stream_id)
        request_headers={
                "Authorization": "Bearer {}".format(self.auth_session.token),
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36",
                "Origin": "https://kayosports.com.au"
        }
        
        try:
            r = requests.request("POST", request_url, headers = request_headers)
            if str(r.status_code) != '200':
                raise Exception('Status: '+str(r.status_code)+ ' trying to access '+ request_url)
            else:
                response_dict = json.loads(r.text)
                print("Stream Data Fetch Successful")
                
                stream_link_data = [response_dict['data'][0]['recommendedStream']]
                if not recommended:
                    stream_link_data += response_dict['data'][0]['alternativeStreams']
                
                #Filter to only contain the formats requested
                if format_filter is not None:
                    stream_link_data = [stream for stream in stream_link_data if stream['mimeType'] == format_filter]

                #Validate the links
                if validate_links == True:
                    stream_link_data = [stream for stream in stream_link_data if validate_stream_link(stream['manifest']['uri'])]

                return {
                    "success": True,
                    "data": [KayoStreamLink(stream) for stream in stream_link_data] 
                    }
        except Exception as e:
            print(e)
            return {
                "success": False
                }

    
    
    
if __name__ == "__main__":
    pass
    # kayo_auth = AuthSession()
    # kayo_session = KayoSession()
    # kayo_session.set_auth_session(kayo_auth)
    # kayo_auth.import_credentials("../TEST_CREDENTIALS.json")
    # profiles_response = kayo_session.get_profiles()
    # if profiles_response.get("success",False):
    #     kayo_session.set_active_profile(profiles_response.get("data")[0])
    # print(kayo_session.active_profile.id)