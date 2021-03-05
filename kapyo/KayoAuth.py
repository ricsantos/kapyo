import json
import requests
import datetime

#Auth0 Tentant client ID used by Kayo
CLIENTID = "qjmv9ZvaMDS9jGvHOxVfImLgQ3G5NrT2"

class AuthSession():
    def __init__(self):
        self.username: str = None
        self.password: str = None
        self.token: str = None
        self.token_expires_in: int = 0
        self.refresh_token: str = None
        self.token_created_at: datetime.datetime = datetime.datetime.now()

    def token_expires_at(self):
        return self.token_created_at + datetime.timedelta(seconds=self.token_expires_in)


    def is_token_expired(self):
        if self.token_expires_at():
            # If 30seconds until token expires, its time to refresh it
            return (datetime.datetime.now()+ datetime.timedelta(seconds=30)) > self.token_expires_at()
        else:
            return True

    def create_credentials_file(self,path):
        try:
            credentials_json = {
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

    def import_credentials(self, path):
        try:
            with open(path) as credentials_file:
                data = json.load(credentials_file)
                self.username = data['USERNAME']
                self.password = data['PASSWORD']
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
            if (response_dict.get("access_token",None) is None):
                raise KayoAuthException
            else:
                self.token = response_dict["access_token"]
                self.token_expires_in = response_dict["expires_in"]
                self.refresh_token = response_dict["refresh_token"]
                self.token_created_at = datetime.datetime.now()
                print("Login Successful")
            return True
        except Exception as e:
            print("AuthSession.login: {}".format(e.message))
            return False

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
            print(response_dict)
            self.token = response_dict["access_token"]
            self.token_expires_in = response_dict["expires_in"]
            self.token_created_at = datetime.datetime.now()
            print("Access Token Refreshed")
            return True
        except:
            print("Response did not contain an access token so something went wrong (Probably Provided Refresh token)")
            return False


class KayoAuthException(Exception):
    """Raised When the Authentication Session Failed to Handle Login Attempt"""
    def __init__(self, message="The Authentication Session failed to Login"):
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    ## Standard Flow for Reference
    #Create a Instance
    kayo_auth = AuthSession()
    
    #Import a Credentials File or Edit the default Credentials File manually
    kayo_auth.create_credentials_file("../CREDENTIALS.json")
    kayo_auth.import_credentials("../CREDENTIALS.json")
    kayo_auth.print_credentials()

    #Login to Kayo using your Credentials
    kayo_auth.login()

    #Check if the Token has expired
    kayo_auth.is_token_expired()

    #If its Expired then refresh the token
    kayo_auth.reset_token()