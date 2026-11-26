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
if __name__=="__main__":
    result=get_playlist_items("2NNJSu3EPmbMlngY2UmC6A", headers_dict)
    print(result)
