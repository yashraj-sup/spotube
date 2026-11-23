import os
import webbrowser
from urllib.parse import urlencode
from dotenv import load_dotenv
load_dotenv()
client_id=os.getenv("client_spotify_id", None)
client_secret=os.getenv("client_spotify_secret", None)
params_dict={
            "client_id":client_id,
            "response_type":"code",
            "redirect_uri":"http://127.0.0.1:8888/callback",
            "scope":"playlist-read-private playlist-modify-private playlist-modify-public", #scopes are the permissions spotify show the user on the agree screen.These three scopes together lets us read playlists, create playlist and ad tracks to them
            "state":"mjsrg",
}
print(params_dict)
base_url="https://accounts.spotify.com/authorize"
authorizing_url=base_url + "?" + urlencode(params_dict)
print(authorizing_url)
webbrowser.open(authorizing_url)