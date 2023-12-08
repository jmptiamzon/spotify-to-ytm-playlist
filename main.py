from dotenv import load_dotenv
from requests import post, get
from ytmusicapi import YTMusic
import os
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
ytmusic = YTMusic("oauth.json")

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
    offset = 0
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    total_track_in_playlist = json.loads(result.content)["total"]
    total_loop_ctr = 1 if total_track_in_playlist < 100 else total_track_in_playlist / 100

    if not total_loop_ctr.is_integer():
        total_loop_ctr += 1

    search_song = []
    
    ctr = 0
    while ctr < total_loop_ctr:
        for items in json_result:
            search_song.append(items["track"]["name"] + " " + items["track"]["album"]["artists"][0]["name"])

        ctr += 1
        offset += 100
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}"
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
    
    return search_song

def get_playlist_name(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["name"]
    return json_result

def write_file(tracks, playlist_name):
    filename = f"track_not_found-{playlist_name}.txt"
    f = open(filename, "w+")

    for track in tracks:
        f.write(track)
        f.write('\n')

def main():
    token = get_token()
    songs_to_search = get_songs_in_playlist(token, "5FXCTC4h2QjcEqaR2ujG9k") #5FXCTC4h2QjcEqaR2ujG9k  JP    2CXRg1frmx7GESmLOJ4OvM random genre
    playlist_name = get_playlist_name(token, "5FXCTC4h2QjcEqaR2ujG9k")
    
    #create playlist
    playlistId = ytmusic.create_playlist(playlist_name, "")

   # for track_name in songs_to_search:
    track_not_found = []
    for track_name in songs_to_search:
        search_result = ytmusic.search(track_name)
        
        if len(search_result) == 0:
            track_not_found.append(track_name)
        else:
            try:  
                ytmusic.add_playlist_items(playlistId, [search_result[0]["videoId"]])
            except:
                track_not_found.append(track_name)

    # wrie dropped tracks
    if len(track_not_found) > 0:
        write_file(track_not_found, playlist_name)

    print("done")


if __name__ == "__main__":
    main()
 