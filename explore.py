import json
import requests
import os
import sys
import isodate
from unidecode import unidecode
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
video2_ids=[]
for item in search_data["items"]:
    video2_ids.append(item["id"]["videoId"])
without_duplication=dict.fromkeys(video2_ids)
#print(without_duplication)   
params2_dict={
    "part":"contentDetails",
    "id":','.join(without_duplication),
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
durations={}
for entry in explore_data["items"]:
    print(entry["id"])
    duration_str=entry["contentDetails"]["duration"]
    duration_object=isodate.parse_duration(duration_str)
    total_seconds=duration_object.total_seconds()
    durations[entry["id"]]=round(total_seconds)
    print(total_seconds)
print(durations)
print (round(len(durations)))
handled_ids=set()
candidates=[]
for item in search_data["items"]:
    videos_id=item["id"]["videoId"]
    if videos_id in handled_ids:
        continue
    if videos_id  not in durations:
        continue
    handled_ids.add(videos_id) #add to the set
    candidates.append({"title":item["snippet"]["title"],
            "channel":item["snippet"]["channelTitle"],
            "duration":durations[videos_id],
            "ID":videos_id
            })
print(len(candidates))
print(candidates[0])
hardcode={"title":"Starboy",
          "artist":"The Weeknd",
          "duration":230,}
def clean(text):
    text=unidecode(text)
    text=text.lower()
    text=text.replace("&", "and")
    return text.replace(" ","")
def passes_artist_gate(track,candidate):
    artist=clean(track["artist"])
    channel=clean(candidate["channel"])
    title=clean(candidate["title"])
    if artist in channel or artist in title:
        return True
    return False
for candidate1 in candidates:
    answer=passes_artist_gate(hardcode,candidate1)
    print(candidate1["title"],answer)

    
    


    
    

           