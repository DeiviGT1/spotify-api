#**********************************************************************************
#Spotify_Handle V0.01
#By:Ben Bellerose
#Description: This is the routing for spotify example.
#**********************************************************************************
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import urlparse, parse_qs
from uvicorn import run
from spotify import app_Authorization, user_Authorization, Album_Data, Profile_Data, Playlist_Data

app = FastAPI()
templates = Jinja2Templates(directory="public")

@app.get("/")
def index():
    # Authorization
    return RedirectResponse("/login")
    

@app.get("/login")
def login():
    auth_url = app_Authorization()
    parsed_url = urlparse(auth_url)
    query_params = parse_qs(parsed_url.query)
    auth_token = query_params.get('code')
    return auth_url 
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback():
    # authorization_header = user_Authorization(auth_url)
    authorization_header = user_Authorization()
    
    #Gathering of profile data
    profile_data = Profile_Data(authorization_header)
    Name = profile_data["display_name"]
    external_urls = profile_data["external_urls"]
    uri = profile_data["uri"]
    href = profile_data["href"]
    followers = profile_data["followers"]["total"]
    images = profile_data["images"]

    #Gathering of playlist data
    playlist_data = Playlist_Data(authorization_header,profile_data)
    x = 0
    playlist_url = []
    playlist_tracks = []
    playlist_titles = []
    while x < len(playlist_data["items"]):
        playlist_tracks.insert(len(playlist_tracks),playlist_data["items"][x]["tracks"]['total'])
        playlist_url.insert(len(playlist_url),playlist_data["items"][x]["tracks"]['href'])
        playlist_titles.insert(len(playlist_titles),playlist_data["items"][x]["name"])
        x = x + 1

    #Gathering of album data
    artist_data = Album_Data(authorization_header,profile_data,50,0)
    x = 0
    album_titles = []
    album_uri = []
    album_label = []
    album_tracknames = []
    album_trackartist = []
    while x < len(artist_data["items"]):
        b = 0
        while b < len(artist_data["items"][x]["album"]["tracks"]['items']):
            album_titles.insert(len(album_titles),artist_data["items"][x]["album"]["name"])
            album_uri.insert(len(album_uri),artist_data["items"][x]["album"]["uri"])
            album_label.insert(len(album_label),artist_data["items"][x]["album"]["label"])
            album_tracknames.insert(len(album_tracknames),artist_data["items"][x]["album"]["tracks"]['items'][b]["name"])
            album_trackartist.insert(len(album_trackartist),artist_data["items"][x]["album"]["tracks"]['items'][b]["artists"][0]['name'])
            b = b + 2
        x = x + 1
    track_hold = {'artist': album_trackartist, 'titles': album_tracknames, 'album': album_titles, 'label': album_label}
    track_hold = zip(track_hold['artist'],track_hold['titles'], track_hold['album'],track_hold['label'])

    # Combine profile and playlist data to display
    display_arr = [profile_data] + [playlist_data["items"][0]] + [artist_data["items"][0]["album"]]
    return str(x)
    # return templates.TemplateResponse("index.html", x = track_hold)

if __name__ == "__main__":
    run(app= "app:app", port=4000, host="localhost", reload=True)