import json
import requests
import sys
from spotify_token import get_access_token
access_token=get_access_token()
headers_dict={
            "Authorization":"Bearer " + access_token,
        } 
def get_playlist_items(playlist_id,headers):
    url= "https://api.spotify.com/v1/playlists/" + playlist_id + "/items"
    response=requests.get(url,headers=headers)
    if response.status_code!=200:
        print(response.status_code, response.text)
        sys.exit()
    return response.json()["items"]
def build_spotify_tracks(items):
    tracks=[]
    skipped=0
    for entry in items:
        song=entry["item"]
        if song is None:
            skipped+=1
            continue
        tracks.append({"title":song["name"],
                    "artist":song["artists"][0]["name"],
                    "duration":round(song["duration_ms"]/1000),
                    })
    print(skipped)
    return tracks
if __name__=="__main__":
    result=get_playlist_items("2NNJSu3EPmbMlngY2UmC6A", headers_dict)
    result2=build_spotify_tracks(result)
    print(result2)
