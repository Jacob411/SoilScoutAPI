import requests
import json


# pulls data from soilscout api
# for now, local files will serve as a database, so as to model the the behaviour once we have a database

# NOTE:
# - Access tokens are valid for 15 minutes.
# - Refresh tokens are valid for 7 days and rotate automatically. There is no blacklist after rotation.

def get_access_token(username : str, password : str) -> dict:
    '''
    Logs into the soilscout api and returns a access and refresh token
    '''
    url = "https://dev.soilscouts.fi/api/v1"
    payload = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    try: 
        response = requests.post(url + "/auth/login/", data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return {"error": "RequestException"}
    return response.json()
 

def get_refresh_token(refresh_token : str) -> dict:
    '''
    Refreshes the access token and returns a new access token
    '''
    url = "https://dev.soilscouts.fi/api/v1"
    payload = {
        "refresh": refresh_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    try: 
        response = requests.post(url + "/auth/token/refresh/", data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return {"error": "RequestException"}
    return response.json()

def verify_access_token(access_token : str) -> dict:
    '''
    Verifies the access token and returns the user id
    '''
    url = "https://dev.soilscouts.fi/api/v1"
    payload = {
        "token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    try: 
        response = requests.post(url + "/auth/token/verify/",data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return {"error": "RequestException"}
    return response.json()



def get_devices(access_token : str) -> dict:
    '''
    Returns a list of devices that the user has access to
    '''
    url = "https://dev.soilscouts.fi/api/v1"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    try: 
        response = requests.get(url + "/devices/", headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return {"error": "RequestException"}
    return response.json()



