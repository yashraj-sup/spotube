import json
import requests
with open("tokens.json", "r", encoding="utf-8") as f:
    tokens=json.load(f)
access_token=tokens["access_token"]
headers_dict={
            "Authorization": "Bearer " + access_token,   
}
response=requests.get("https://api.spotify.com/v1/me/playlists",params={"limit": 10,"offset":0,}, headers=headers_dict)                                                               
print(response.status_code)
if response.status_code==200:
    print(list(response.json().keys()))

