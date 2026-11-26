import json
import requests
import os
import sys
from dotenv  import load_dotenv
load_dotenv()
client_id=os.getenv("client_spotify_id", None)
client_secret=os.getenv("client_spotify_secret", None)
def get_access_token():
    with open("tokens.json", "r", encoding="utf-8") as f:
        tokens=json.load(f)
    token_url="https://accounts.spotify.com/api/token"
    refresh_data={
            "grant_type":"refresh_token",
            "refresh_token":tokens["refresh_token"],
    }
    response=requests.post(token_url, data=refresh_data, auth=(client_id, client_secret))
    if response.status_code!=200:
        print(response.status_code,response.text)
        sys.exit()
    new_data=response.json()
    tokens["access_token"]=new_data["access_token"]
    if "refresh_token" in new_data:
        tokens["refresh_token"]=new_data["refresh_token"]
    with open("tokens.json","w", encoding="utf-8") as tokens_file:
        json.dump(tokens,tokens_file, indent=4, ensure_ascii=False)
    return tokens["access_token"]
if __name__=="__main__":
    token=get_access_token()
    with open("tokens.json", "r", encoding="utf-8") as f:
        tokens1=json.load(f)
    print(len(token))
    print(list(tokens1.keys()))

