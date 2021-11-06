import pathlib
from dataclasses import dataclass
import json

@dataclass
class Credentials:
    username: str
    password: str

    @classmethod
    def from_credential_file(cls,path):
        try:
            with open(path) as credentials_file:
                data = json.load(credentials_file)
                return cls(username = data['USERNAME'], password=data['PASSWORD'])
        except IOError as ioe:
            print("IO error occurred while trying to read from credentials file")
            raise ioe
        except Exception as ex:
            print("Unexpected error occurred while trying to read from credentials file")
            raise ex

    @classmethod
    def from_login_details(cls, username: str, password:str):
        return cls(username=username,password=password)

    def __repr__(self):
        return self.username + '\n' + self.password

    def export_credentials_file(self, path: pathlib.Path):
        try:
            credentials_json = {
                "USERNAME":self.username,
                "PASSWORD":self.password
            }
            with open(path, 'w+') as credentials_file:
                json.dump(credentials_json, credentials_file)
        except IOError as ioe:
            print('IO Error while trying to write to credentials file')
            raise ioe
        except Exception as ex:
            print('Unexpected error occurred while trying to write to credentials file')
            raise ex