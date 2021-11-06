import requests
import logging
import time
import json


def retry(method):
    total_tries = 3
    delay = 0.5
    def wrapper(ref,*args,**kwargs):
        _tries = 1
        while _tries <= total_tries:
            try:
                logging.debug(f"Attempt {_tries}")
                return method(ref,*args,**kwargs)
            except Exception as ex:
                _tries += 1
                if _tries > total_tries:
                    logging.debug(f"Out of Retry Attempts")
                    raise ex
                time.sleep(delay)
    return wrapper

def authenticate(method):
    def authenticated_method(ref, *args, **kwargs):
        return method(ref, *args, **kwargs, token=ref.token())
    return authenticated_method

def create_empty_credentials_file(credentials_path):
        try:
            credentials_json = {
                "USERNAME": "yourkayoemail@domain.com",
                "PASSWORD": "Y0urP@s5w0rd"
            }
            with open(credentials_path, 'w+') as credentials_file:
                json.dump(credentials_json, credentials_file)
        except:
            "Something went wrong with creating the credentials file"


def create_credentials_file(credentials_path, username, password):
    try:
        credentials_json = {
            "USERNAME": username,
            "PASSWORD": password
        }
        with open(credentials_path, 'w+') as credentials_file:
            json.dump(credentials_json, credentials_file)
    except:
        "Something went wrong with creating the credentials file"


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

