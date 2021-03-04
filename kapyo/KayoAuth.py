import json
import requests
import datetime

class AuthSession():
    def __init__(self):
        username: str
        password: str
        client_id: str
        token: str
        token_expires_in: int
        refresh_token: str
        profile: str
        token_created_at: datetime.datetime

    def token_expires_at(self):
        return self.token_created_at + datetime.timedelta(seconds=self.token_expires_in)

    def create_credentials_file(self,path):
        try:
            credentials_json = {
                "CLIENTID":"Your Client Id Goes Here",
                "USERNAME":"yourkayologin@domain.com",
                "PASSWORD":"Y0urP@s5w0rd"
            }
            with open(path, 'w+') as credentials_file:
                json.dump(credentials_json, credentials_file)
        except:
            "Something went wrong with creating the credentials file"


    def print_credentials(self):
        print(self.username)
        print(self.password)
        print(self.client_id)

    def import_credentials(self, path):
        try:
            with open(path) as credentials_file:
                data = json.load(credentials_file)
                self.username = data['USERNAME']
                self.password = data['PASSWORD']
                self.client_id = data['CLIENTID']
        except Exception as e:
            print("A error occured when importing credentials")

    def login(self):
        #Use the Username & Password to make a request to Kayo for your access token       
        requestUrl = "https://auth.kayosports.com.au/oauth/token"
        requestJson = "{\n"+\
                          " \"audience\":\"kayosports.com.au\",\n"+\
                          "\"grant_type\":\"http://auth0.com/oauth/grant-type/password-realm\",\n"+\
                          "\"scope\": \"openid offline_access\", \n"+\
                          "\"realm\": \"prod-martian-database\",\n"+\
                          "\"client_id\": \""+self.client_id+"\",\n"+\
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
            self.token_created_at = datetime.datetime.now()
            print("Login Successful")
        except Exception as e:
            print("Response did not contain an access token so something went wrong (Probably Username or Password)")
            print(response_dict)

    def reset_token(self):
        #use the refresh token to update the Bearer Token
        requestUrl = "https://auth.kayosports.com.au/oauth/token"
        requestJson = "{\n"+\
                          " \"redirectUri\":\"https://kayosports.com.au/login\",\n"+\
                          "\"client_id\": \""+self.client_id+"\",\n"+\
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
            print(response_dict)
            self.token = response_dict["access_token"]
            self.token_expires_in = response_dict["expires_in"]
            self.token_created_at = datetime.datetime.now()
            print("Access Token Refreshed")
        except:
            print("Response did not contain an access token so something went wrong (Probably Provided Refresh token)")


if __name__ == "__main__":
    kayo_auth = AuthSession()
    kayo_auth.create_credentials_file("../CREDENTIALS.json")
    kayo_auth.import_credentials("../CREDENTIALS.json")
    kayo_auth.print_credentials()
    kayo_auth.login()
    kayo_auth.reset_token()