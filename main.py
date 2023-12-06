from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {    
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + auth_base64
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def get_songs_in_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=10"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]

    #print(json_result[0])

    search_song = []
    for items in json_result:
        search_song.append(items["track"]["name"] + " " + items["track"]["album"]["artists"][0]["name"])
    
    if len(json_result) == 0:
        print("NULL")
        return None
    
    return search_song

def get_playlist_name(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)

token = get_token()
songs_to_search = get_songs_in_playlist(token, "2CXRg1frmx7GESmLOJ4OvM")



#print(result)
