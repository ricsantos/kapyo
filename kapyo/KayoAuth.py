import json
import requests

#CONSTANTS
CLIENTID="Your Client Id Goes Here"
USERNAME="yourkayologin@domain.com"
PASSWORD="Y0urP@s5w0rd"

class AuthSession():
    def __init__(self):
        username: str
        password: str
        token: str
        token_expires_in: int
        refresh_token: str
        profile: str

    def login(self, username: str, password: str):
        #Use the Username & Password to make a request to Kayo for your access token
        self.username = username
        self.password = password

        
        requestUrl = "https://auth.kayosports.com.au/oauth/token"
        requestJson = "{\n"+\
                          " \"audience\":\"kayosports.com.au\",\n"+\
                          "\"grant_type\":\"http://auth0.com/oauth/grant-type/password-realm\",\n"+\
                          "\"scope\": \"openid offline_access\", \n"+\
                          "\"realm\": \"prod-martian-database\",\n"+\
                          "\"client_id\": \""+CLIENTID+"\",\n"+\
                          "\"username\": \""+ self.username+"\",\n"+\
                          "\"password\": \""+ self.password+"\"\n}"
        requestHeaders={
                "Content-Type": "application/json",
                "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
        }
        try:
            print("Contacting Kayo Servers with Login Details")
            r = requests.request("POST", requestUrl, data=requestJson, headers=requestHeaders)
            response_dict = json.loads(r.text)
            self.token = response_dict["access_token"]
            self.token_expires_in = response_dict["expires_in"]
            self.refresh_token = response_dict["refresh_token"]
            print("Login Successful")
        except:
            print("Response did not contain a access token so something went wrong (Probably Username or Password)")

    def reset_token(self):
        #use the refresh token to update the Bearer Token
        requestUrl = "https://auth.kayosports.com.au/oauth/token"
        requestJson = "{\n"+\
                          " \"redirectUri\":\"https://kayosports.com.au/login\",\n"+\
                          "\"client_id\": \""+CLIENTID+"\",\n"+\
                          "\"grant_type\":\"refresh_token\",\n"+\
                          "\"refresh_token\": \""+self.refresh_token+"\" \n}"
        requestHeaders={
                    "Content-Type": "application/json",
                    "User-Agent": "User-Agent: Mozilla/5.0 {Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/44.0.2403.89 Safari/537.36"
                }
        
        try:
            print("Contacting Kayo Servers with Refresh Token")
            r = requests.request("POST", requestUrl, data=requestJson, headers=requestHeaders)
            response_dict = json.loads(r.text)
            self.token = response_dict["access_token"]
            self.token_expires_in = response_dict["expires_in"]
            self.refresh_token = response_dict["refresh_token"]
            print("Tokens Refreshed")
        except:
            print("Response did not contain a access token so something went wrong (Probably Provided Refresh token)")


if __name__ == "__main__":
    kayo_auth = AuthSession()
    kayo_auth.login(USERNAME,PASSWORD)
    kayo_auth.reset_token()
