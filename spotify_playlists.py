import json
import requests
from spotify_token import get_access_token
access_token=get_access_token()
headers_dict={
            "Authorization": "Bearer " + access_token,   
}
response=requests.get("https://api.spotify.com/v1/me/playlists",params={"limit": 10,"offset":0,}, headers=headers_dict)                                                               
print(response.status_code)
if response.status_code==200:
    print(list(response.json().keys()))
data=response.json()
print(type(data["items"]))
print(len(data["items"]))
print(list(data["items"][0].keys()))
for item in data["items"]:
    print(item["name"], item["owner"]["id"])
    print(item["id"])
    print(item["items"])
print(data["total"])
print(data["next"])


