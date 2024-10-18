import os
import json
from api_utils import *


class SoilScoutClient:
    def __init__(self, username : str, password : str):
        self.username = username
        self.password = password
        token = get_access_token(self.username, self.password)
        self.access_token = token["access"]
        self.refresh_token = token["refresh"]
        self.devices = []
     
    def login_flow(self):
        '''
        Function that offers a more complicated login flow. Less API calls, but would take more database read/writes (WILL NOT BE USED FOR NOW)
        '''

        # Check to see if there is a refresh token
        if os.path.exists("data/token.json"):
            with open("data/token.json", "r") as f:
                if "refresh" in json.load(f):
                    self.refresh_token = json.load(f)["refresh"]
                else:
                    self.refresh_token = ""
                 
        # If there is no refresh token, then login
        if self.refresh_token == "":
            access_token = get_access_token(self.username, self.password)["access"]
            self.access_token = access_token
            #write the raw json access token to a file
            with open("data/token.json", "w") as f:
                json.dump(access_token, f)

        # Try to use the refresh token to get an access token
        else:
            # If there is a refresh token, then check to see if it is valid
            curr_token = get_refresh_token(self.refresh_token)
            if "access" in curr_token:
                # If it is valid, then use it
                self.access_token = curr_token["access"]
                self.refresh_token = curr_token["refresh"]
                #write the raw json access token to a file
                with open("data/token.json", "w") as f:
                    json.dump(curr_token, f)
            else:
                # If it is not valid, then login
                access_token = get_access_token(self.username, self.password)["access"]
                self.access_token = access_token["access"]
                self.refresh_token = access_token["refresh"]
                #write the raw json access token to a file
                with open("data/token.json", "w") as f:
                    json.dump(access_token, f)
    
    def get_devices(self):
        # Get the devices
        devices = get_devices(self.access_token)
        self.devices = devices
        return devices



