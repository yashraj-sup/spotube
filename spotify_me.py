import json
import requests
with open("tokens.json", "r", encoding="utf-8") as f:
    tokens=json.load(f)
access_token=tokens["access_token"]
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

