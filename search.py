import json
import isodate
import requests
import sys
import os
from dotenv import load_dotenv
load_dotenv()
url="https://www.googleapis.com/youtube/v3/search"
api_key=os.getenv("youtube_api_key", None)
if not api_key:
    print("check youtube_api_key in  .env file")
    sys.exit()
params_dict={
    "part":"snippet",
    "q":"STARBOY BY THE WEEKND",
    "type":"video",
    "maxResults": 10,
    "key":api_key,
}
response=requests.get(url, params=params_dict)
print(response.status_code)
if response.status_code!=200:
    print(response.text)
    sys.exit()
search_data=response.json()
with open("search_response.json", "w", encoding="utf-8") as search_response:
    json.dump(search_data,search_response,indent=4,ensure_ascii=False)

for item in search_data["items"]:
    print(item["snippet"]["title"], item["snippet"]["channelTitle"],item["id"]["videoId"]) #getting title,channelname and videoId from the items list from the search_response.json file
#every run of search.py costs 100 units while explore.py is free