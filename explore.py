import json
import requests
import os
import sys
from dotenv import load_dotenv
load_dotenv()
url2="https://www.googleapis.com/youtube/v3/videos"
api_key=os.getenv("youtube_api_key",None)
if not api_key:
    print("check youtube_api_key in .env file",)
    sys.exit()
with open("search_response.json", "r", encoding="utf-8") as search_response:
    search_data=json.load(search_response) # process of deserialization: where json.load reads data directly froma file and converts it into a native pytgon object
#for item in search_data["items"]:
    #print(item["snippet"]["title"], item["snippet"]["channelTitle"],item["id"]["videoId"]) #getting title,channelname and videoId from the items list from the search_response.json file
video_ids=['34Na4j8AVgA','xizN47Box_Y','Rif-RTvmmss','vuT_bXzhqhY','plnfIj7dkJE','y76Te50yj20','SsRXJnzas2s','HR3NP_wxBl0','dMMUH_ZpbB0','dMMUH_ZpbB0']
params2_dict={
    "part":"contentDetails",
    "id":','.join(video_ids),
    "key":api_key,
}
video_response=requests.get(url2,params=params2_dict)
print(video_response.status_code)
if video_response.status_code!=200:
    print(video_response.text)
    sys.exit()
explore_data=video_response.json()
print(len(explore_data["items"]))
with open("video_response.json", "w", encoding="utf-8") as out_file:
    json.dump(explore_data,out_file,indent=4,ensure_ascii=False)#sterialization:convert a python object into a json-formatted stream and write it directly to a file-like object



           