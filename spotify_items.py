import json
import requests
with open("tokens.json", "r", encoding="utf-8") as f:
    tokens=json.load(f)
access_token=tokens["access_token"]
headers_dict={
            "Authorization":"Bearer " + access_token,
        } 
def gives_len_list(url,headers):
    response=requests.get(url,headers=headers_dict)
    if response.status_code==200:
        print(list(response.json().keys()))
        print(len(response.json()["items"]))
    return response.text
result=gives_len_list("https://api.spotify.com/v1/playlists/2NNJSu3EPmbMlngY2UmC6A/items",headers_dict)
print(result)