from spotify_token import get_access_token
from spotify_items import get_playlist_items, build_spotify_tracks
from explore import search, get_duration, build_candidates, gives_winner
import json
import sys
if __name__=="__main__":
    headers_dict={"Authorization": "Bearer " + get_access_token()}
    calling_get_playlist_items=get_playlist_items("2NNJSu3EPmbMlngY2UmC6A",headers_dict)
    tracks=build_spotify_tracks(calling_get_playlist_items)
    track=tracks[3]
    search_result=search(track["title"], track["artist"])
    if search_result is None:
        print("request failed")
        sys.exit()
    with open("search_dracula.json", "w", encoding="utf-8") as f:
        json.dump(search_result, f, indent=4, ensure_ascii=False)
    duration_result=get_duration(search_result)
    if duration_result is None:
        print("request failed")
        sys.exit()
    with open("video_dracula.json", "w", encoding="utf-8") as v:
        json.dump(duration_result, v, indent=4, ensure_ascii=False)
    candidates=build_candidates(search_result, duration_result)
    winner, score=gives_winner(candidates, track)
    if winner is None:
        print("no match")
        sys.exit()
    print(track["title"], "-", track["artist"])
    print(winner["title"], "|", winner["channel"], "|", winner["ID"], score)

        
    



