import requests
import base64
import datetime # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
import json


from project.helpers import expired, counter
from project import app


# formats url for api request, playlist or album
def formatUrl(url):
    # is it album or playlist?
    if "album" in url:
        url_type = "albums"
    else:
        url_type = "playlists"

    # find start and end point of playlist/album ID
    id_start = url.find(url_type[:-1]) + len(url_type[:-1]) + 1

    if "?si=" in url:
        id_end = url.find("?si=")
        # set ID to separate variable
        url_id = url[id_start:id_end]
    else:
        url_id = url[id_start:]
        

    # format url
    request_url = f"https://api.spotify.com/v1/{url_type}/{url_id}/tracks"

    return request_url
    

# parse url, extract spotify ID
def getID(url):
    # is it album or playlist?
    if "album" in url:
        url_type = "albums"
    else:
        url_type = "playlists"

    # find start and end point of playlist/album ID
    id_start = url.find(url_type[:-1]) + len(url_type[:-1]) + 1
    id_end = url.find("?si=")

    # set ID to separate variable
    url_id = url[id_start:id_end]

    return url_id




# request new api acess token
def getNewToken():
    # format client credentials for API token request
    # client_id = os.environ.get("API_KEY_SPOTIFY")
    # client_secret = os.environ.get("API_SECRET_SPOTIFY")
    with open("tokens.json", "r") as file:
        tokens = json.load(file)
    client_id = tokens["API_KEY_SPOTIFY"]
    client_secret = tokens["API_SECRET_SPOTIFY"]

    client_creds = f"{client_id}:{client_secret}"
    # spotify requires base64 encode
    client_creds = client_creds.encode()
    client_creds_b64 = base64.b64encode(client_creds)
    # convert it to string
    client_creds_b64 = client_creds_b64.decode()

    # API request URL
    token_url = "https://accounts.spotify.com/api/token"
    # data and headers for API request
    token_data = {"grant_type": "client_credentials"}
    token_headers = {"Authorization": f"Basic {client_creds_b64}"}

    # make API request
    req = requests.post(token_url, data=token_data, headers=token_headers)

    # format response
    response = req.json()
    token = response["access_token"]

    # format expiration from seconds to datetime, to check it later
    expires_in = response["expires_in"]
    expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    expires = expires.strftime("%Y-%m-%d %H:%M:%S")

    # put new token and expiration date in to dictionary, to store it in json file
    spotify_data = {
        "token": token,
        "expires": expires
    }

    # open and read existing json file with token dictionaries
    with open("tokens.json", "r") as file:
        data = json.load(file)

    # update dict info with new token data
    data["spotify"] = spotify_data

    # write updated dictionary to json file
    with open("tokens.json", "w") as file:
        json.dump(data, file, indent=4, default=str)

    return token


# get old token from file or call function to get the new one
def getToken():
    # open file and check if token in file is expired
    with open("tokens.json", "r") as file:
        data = json.load(file)

    token = data["spotify"]["token"]
    expires = data["spotify"]["expires"]

    # check if old token expired and if it is, get new token and return it
    # else return old token, from json file
    if expired(expires):
        return getNewToken()
    else:
        return token


# spotify api request
def call(url, token):
    # declare headers for api call
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # make a first call
    try:
        request = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        raise e

    # check status code
    if not request.status_code == 200:
        return request.status_code
    if not request:
        return request.status_code

    request = request.json()

    # return everything if request for total info about playlist
    if not "tracks" in url:
        return request


    # make data list of dicts with items
    data = []
    data.append(request["items"])

    # total tracks in playlist
    total = request["total"]

    # YT api quota check
    if total > (1000 - counter()):
        raise -1

    # if there is more then 100 tracks in playlist, make additional calls
    # 100 tracks is maximum, that spotify api returns at once
    if total > 100:
        offset = 0
        # request remaining tracks in playlist
        while True:
            # break, if total is less then offset
            if total < offset:
                break

            # change offset
            offset = offset + 100

            # update url
            query = f"?offset={offset}"
            new_url = f"{url}{query}"

            # make additional calls while total is more then offset
            try:
                req = requests.get(new_url, headers=headers)
            except requests.exceptions.RequestException as e:
                raise e

            # check status code
            if not req.status_code == 200:
                return req.status_code

            # append returned items to data dict
            req = req.json()
            req = req["items"]

            data.append(req)


    # return converted to dicts
    return data


# request total info about playlist
def info(url):
    # To get list of tracks with names and artists
    # Get spotify api token
    token = getToken()
    # Format url
    url = formatUrl(url)

    # request API everything about playlist
    info = call(url[:-7], token)

    return info


# convert api response to usable information
def tracks(url):
    # To get list of tracks with names and artists
    # Get spotify api token
    token = getToken()

    # Format url
    url = formatUrl(url)

    # request API tracks
    data = call(url, token)

    tracks = []

    # for each item in data, returned by call to spotify api
    for answer in data:
        for dictionary in answer:
            # try playlist response format, if KeyError, means response is in album format
            try:
                track = {
                    "artist": dictionary["track"]["artists"][0]["name"],
                    "name": dictionary["track"]["name"],
                    # "album": dictionary["track"]["album"]["name"]
                }
            except KeyError:
                track = {
                    "artist": dictionary["artists"][0]["name"],
                    "name": dictionary["name"]
                }

            # append result to list of tracks
            tracks.append(track)

    return tracks


