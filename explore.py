import json
import requests
import os
import sys
import isodate
import re
from rapidfuzz import fuzz
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
    if artist in channel or artist in title: # containment: in requires the letters to sit next to each other
        return True
    return False
#for candidate1 in candidates:
 #   answer=passes_artist_gate(hardcode,candidate1)
  #  print(candidate1["title"],answer)
flags_dict={"remix":25,
            "live":25,
            "lyric":50,
            "lyrics":50,
            "sped up":50,
            "instrumental":50,
            "cover":50,
            "slowed":50,
}
def flags_found(title):
    title=unidecode(title)
    title=title.lower()
    title=re.sub(r"[^\w\s]", " ", title)
    title=" ".join(title.split())
    title=" "+ title + " "
    flags_list=[]
    for flag in flags_dict:
        flag1=" "+ flag + " "
        if flag1 in title: #need to look for padded word in title
            flags_list.append(flag) #unpadded word with the output
    return flags_list
#for candidate in candidates:
 #   print(candidate["title"],flags_found(candidate["title"]))
def penalty_function(title):
    found=flags_found(title)
    penalties=[]
    for flag3 in found:
        penalties.append(flags_dict[flag3])
    return sum(penalties)
#for candidate in candidates:
 #   print(candidate["title"],penalty_function(candidate["title"]))
def cleaned_song_name(title,artist):
    text=unidecode(title)
    artist=unidecode(artist)
    text=re.sub(r"\(.*?\)", " ", text)
    text=re.sub(r"\[.*?\]", " ", text)
    text=re.sub(r"\b(?:feat|ft)\b.*", " ", text, flags=re.IGNORECASE)
    text=re.sub(re.escape(artist), " ", text, flags=re.IGNORECASE)
    text=text.replace("&", " and ")
    text=re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.lower().split())
cleaned_spotify_title=cleaned_song_name(hardcode["title"], hardcode["artist"])
cutoff=50
def title_penalty_function(clean_candidate,cleaned_spotify_title):
    score1_ratio=fuzz.ratio(clean_candidate,cleaned_spotify_title)
    if score1_ratio<cutoff:
        return 0
    else:
        return (score1_ratio-cutoff)/(100-cutoff)*60
cutoff2=30
duration_points = 40
def duration_penalty_function(candidate_duration, spotify_tracks_duration):
    diff = abs(candidate_duration - spotify_tracks_duration)
    if diff >= cutoff2:
        return 0
    return duration_points * (1 - diff / cutoff2)
def candidate_into_single_total(candidate,spotify_track):
    if  not passes_artist_gate(spotify_track,candidate):
        return None
    cleaned_candidate_title=cleaned_song_name(candidate["title"], spotify_track["artist"])
    title_points=title_penalty_function(cleaned_candidate_title,cleaned_spotify_title)
    duration_points_earned=duration_penalty_function(candidate["duration"],spotify_track["duration"])
    flag_penalty=penalty_function(candidate["title"])
    total_points=max(0,duration_points_earned+title_points-flag_penalty)
    return total_points
best_total=None
best_candidate=None
best_rank=None
def rank_number(candidate,spotify_track):
    if clean(spotify_track["artist"]) in clean(candidate["channel"]) and "vevo" in clean(candidate["channel"]):
        return 2
    elif clean(spotify_track["artist"]) in clean(candidate["channel"]) and "topic" in clean(candidate["channel"]):
        return 1
    return 0
for candidate in candidates:
    total=candidate_into_single_total(candidate,hardcode)
    if total is None:
        continue
    total=round(total,2)
    rank=rank_number(candidate, hardcode)
    if best_total is None or total>best_total or (total==best_total and rank>best_rank):
        best_total=total
        best_candidate=candidate
        best_rank=rank
    print(candidate["title"],total,rank)
print(best_candidate)



    
#for candidate in candidates:
 #   print(candidate["title"], "->", cleaned_song_name(candidate["title"], hardcode["artist"]))

    



           
           
    


     


    
    


    