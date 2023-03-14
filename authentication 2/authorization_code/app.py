from flask import Flask, request, redirect, g, render_template
import json
from pymongo import MongoClient
from data import read_mongo, delete_all_documents, analyze_average_popularity_per_album, Mongo_Song_Data
from spotify import app_Authorization, user_Authorization, Album_Data, Profile_Data, Playlist_Data, Song_Data

app = Flask(__name__, static_url_path='/static', template_folder='public')

@app.route("/")
def index():
    # Authorization
    return render_template("index.html")

@app.route("/login")
def login():
    # Authorization
    auth_url = app_Authorization()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    authorization_header = user_Authorization()

    #Gathering of profile data
    profile_data = Profile_Data(authorization_header)
    user_id = profile_data["id"]
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
    playlist_titles = []
    playlist_track_count = []
    playlist_track_url = []
    songs = []
    while x < len(playlist_data["items"]):
        playlist_track_count.insert(len(playlist_track_count),playlist_data["items"][x]["tracks"]['total'])
        playlist_url.insert(len(playlist_url),playlist_data["items"][x]["tracks"]['href'])
        playlist_titles.insert(len(playlist_titles),playlist_data["items"][x]["name"])
        playlist_track_url.insert(len(playlist_track_url),playlist_data["items"][x]["tracks"]['href'])
        x = x + 1
    for items in playlist_data["items"]:
        playlist_name = items["name"]
        url = items["tracks"]["href"]
        song_data = Song_Data(authorization_header,url)
        for song in song_data["items"]:
            songs.insert(
                len(songs),
                {
                    "id":song["track"]["id"],
                    "name":song["track"]["name"],
                    "artist":song["track"]["artists"][0]["name"],
                    "playlist_name":playlist_name,
                    "added_at":song["added_at"],
                    "user_id":user_id,
                    "duration_ms":song["track"]["duration_ms"],
                    "popularity":song["track"]["popularity"],
                    "explicit":song["track"]["explicit"],
                    "amount_available_markets":len(song["track"]["available_markets"]),
                }
            )

    delete_all_documents({'info.user_id': user_id})
    Mongo_Song_Data(songs)
    avg_per_playlist = analyze_average_popularity_per_album(user_id)
    return render_template("playlist.html", avg_per_playlist=avg_per_playlist)

if __name__ == "__main__":
    app.run(debug = True, port=4000, host="localhost")