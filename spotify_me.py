import json
import requests
from spotify_token import get_access_token
access_token=get_access_token()
headers_dict={
        "Authorization":"Bearer " + access_token,
}
response=requests.get("https://api.spotify.com/v1/me", headers=headers_dict)
me=response.json()
print(response.status_code)
if response.status_code==200:
    print(me["display_name"])
else:
    print(response.text)
print(me['id'])

