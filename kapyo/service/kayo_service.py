from kapyo.dataclass.profile import KayoProfile
from kapyo.dataclass.token import KayoAuthToken
from kapyo.dataclass.stream_link import KayoStreamLink
from kapyo.dataclass.event import KayoEvent
from kapyo.helpers import retry

import json
import requests


class KayoService:
    @staticmethod
    def default_headers(token_obj):
        return {
                "Authorization": f"Bearer {token_obj.token}",
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
            }


    @retry
    def get_profiles(self,token:KayoAuthToken):
        request_url = "https://profileapi.kayosports.com.au/user/profile"
        request_headers = self.default_headers(token)
        r = requests.request("GET", request_url, headers=request_headers)
        r.raise_for_status()
        response_dict = json.loads(r.text)
        return [KayoProfile(profile) for profile in response_dict]

    @retry
    def get_profile_events(self, token:KayoAuthToken, profile:KayoProfile):
        request_url = "https://vccapi.kayosports.com.au/v2/content/types/landing/names/sports"
        request_headers = self.default_headers(token)
        request_params = dict()
        request_params['profile'] = profile.id
        r = requests.request("GET", request_url, params = request_params, headers=request_headers)
        r.raise_for_status()
        response_dict = json.loads(r.text)
        return [KayoEvent(id= event["data"]["asset"]["id"],
                          title= event["data"]["asset"]["title"],
                          description= event["data"]["asset"]["description"],
                          sport= event["data"]["asset"]["sport"],
                          series_id= event["data"]["asset"]["series-id"],
                          category_id= event["data"]["asset"]["category"]["id"])
                for event in response_dict[0].contents]

    @retry
    def get_series_events(self,token: KayoAuthToken,sport: str = None, series: str = None):
        request_url = "https://vccapi.kayosports.com.au/v2/content/types/landing/names/series"
        request_headers = self.default_headers(token)
        request_params = dict()
        if sport is not None:
            request_params['sport'] = sport
        if series is not None:
            request_params['series'] = series
        r = requests.request("GET", request_url, params = request_params, headers = request_headers)
        r.raise_for_status()
        response_dict = json.loads(r.text)
        return [KayoEvent.from_dict(event) for event in response_dict]


    @retry
    def get_stream_manifests(self, token:KayoAuthToken,stream_id:str, recommended: bool=False, format_filter: str = None):
        request_url = f"https://vmndplay.kayosports.com.au/api/v1/asset/{stream_id}/play?fields=alternativeStreams"
        request_headers = self.default_headers(token)
        request_headers["Origin"]="https://kayosports.com.au"
        r = requests.request("POST", request_url, headers=request_headers)
        r.raise_for_status()
        response_dict = json.loads(r.text)

        stream_link_data = [response_dict['data'][0]['recommendedStream']]
        if not recommended:
            stream_link_data += response_dict['data'][0]['alternativeStreams']

        # Filter to only contain the formats requested
        if format_filter is not None:
            stream_link_data = [stream for stream in stream_link_data if stream['mimeType'] == format_filter]

        return [KayoStreamLink(stream) for stream in stream_link_data]

