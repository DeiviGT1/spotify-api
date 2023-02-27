from flask import Flask, request, redirect, session, render_template
import requests
import random
import string
import spotipy
import urllib
import time
import urllib.parse
import base64
import pandas as pd
from datetime import datetime, timedelta
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlparse
import json

app = Flask(__name__, template_folder="public")

client_id = '4e90e934295b4cb984d8ac90deab6d69' 
client_secret = '43f77b42f24f4ac4bb75552326377c5d'
redirect_uri = 'http://127.0.0.1:4000/callback'
stateKey = 'user-top-read'

headers = ({
            'Content-Type': "application/json",
            "Authorization": f'Bearer  {client_secret}'
        })


def generate_random_string(length):
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@app.before_request
def before_request():
  cookies = {}
  cookie_header = request.headers.get('Cookie')
  if cookie_header:
    cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_header.split('; ')}

  # Add parsed cookies to request object
  request.cookies = cookies

@app.route('/')
def index():
  return render_template('index.html')

@app.route("/login")
def login():
    client_id = "YOUR_CLIENT_ID"
    redirect_uri = "http://localhost:5000/callback"
    scopes = ["user-read-recently-played"]

    # Redirect user to Spotify authorization endpoint
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes)
    }
    url = auth_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    return redirect(url)

@app.route("/callback")
def callback():
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    redirect_uri = "http://localhost:5000/callback"

    # Exchange authorization code for access token
    authorization_code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"}
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception("Failed to retrieve access token")

    access_token = response.json()["access_token"]
    return access_token


@app.route('/saved_songs')
def saved_songs():

  sp_oauth = spotipy.Spotify(auth=session['access_token'])
  offset = 0
  limit = 50
  arr = []
  while True and offset < 100:
    results = sp_oauth.current_user_saved_tracks(limit=limit, offset=offset)
    for i in results['items']:
      dict_ = {}
      dict_["name"] = i['track']['name']
      dict_["date"] = i['added_at']
      arr.extend([dict_])
    offset += len(results['items'])
    if len(results['items']) < limit:
        break
  
  
  return render_template('app.html', songs=arr)

@app.route('/user_top_artists_and_content')
def user_top_artists_and_content():
  stateKey = 'user-top-read'
  sp_oauth = spotipy.Spotify(auth=session['access_token'])
  results = sp_oauth.current_user_top_tracks()
  return results
  arr = []
  for i in results['items']:
    dict_ = {}
    dict_["id"] = i['id']
    dict_["name"] = i['name']
    dict_["duration"] = i['duration_ms']
    for artist in i['artists']:
      dict_[f"artist_{artist}"] = artist['name']
    for album in i["album"]:
      dict_[f"album_{album}"] = album['name']
      dict_["release_date"] = album['release_date']
      dict_["total_tracks"] = album['total_tracks']
    arr.extend([dict_])


  return arr

@app.route('/user_playback_state')
def user_playback_state():
  
  stateKey = 'user-read-playback-state'
  sp_oauth = spotipy.Spotify(auth=session['access_token'])
  results = sp_oauth.current_user_playlists()
  
  for i in results['items']:
    dict_ = {}
    dict_["id"] = i['id']
    dict_["name"] = i['name']
    dict_["owner"] = i['owner']['display_name']
    
  return None

@app.route('/recently_played')
def recently_played():
  stateKey = 'user-read-recently-played'
  sp_oauth = spotipy.Spotify(auth=session['access_token'])
  date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
  arr = []
  results = sp_oauth.current_user_recently_played(limit=50)
  return results
  last_6_months = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000) # get last 6 months
  before = int(time.time() * 1000) # current time in milliseconds
  results = sp_oauth.current_user_recently_played(limit=50, before=None)
  return results
  while before > last_6_months:
    if len(results['items']) == 0:
      break
    arr += results
    before = int(datetime.strptime(results['items'][-1]['played_at'], date_format).timestamp() * 1000)

  my_dict = {}
  for index, k in enumerate(arr):
    my_dict[index] = f"{k}"
  df = pd.DataFrame.from_dict(my_dict, orient='index')
  df.to_json('data.json')
  return {"finished":"finished"}

  for i in results_final:
    dict_ = {}
    dict_["played_at"] = datetime.strptime(i['played_at'], date_format)
    dict_["id"] = i['track']['id']
    dict_["name"] = i['track']['name']
    for j in i['track']['artists']:
      dict_[f"artist_{j}"] = j['name']
    dict_["duration"] = i['track']['duration_ms']
    dict_["popularity"] = i['track']['popularity']
    arr.extend([dict_])

  return arr


@app.route('/playlists')
def playlists():
  stateKey = 'playlist-read-private'
  sp_oauth = spotipy.Spotify(auth=session['access_token'])
  arr = []
  results = sp_oauth.current_user_playlists()

  for i in results['items']:
    dict_ = {}
    dict_["name"] = i["name"]
    dict_["owner"] = i["owner"]["display_name"]
    dict_["tracks"] = i["tracks"]["total"]
    arr.extend([dict_])


  return arr

@app.route('/refresh_token')
def refresh_token():
  code = request.args.get('code')
  refresh_token = session['refresh_token']
  post_data = {'code': code, 
      'redirect_uri': redirect_uri, 
      'grant_type': 'authorization_code',
      "refresh_token": refresh_token,
      "client_id": client_id,
      "client_secret": client_secret,
      "redirect_uri": redirect_uri,
      }

  auth_response = requests.post('https://accounts.spotify.com/api/token', data=post_data, timeout=30)
  if auth_response.status_code == 200:
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    session['access_token'] = access_token
    return access_token
  else:
    return 'Error: unable to refresh token', 400

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.run(host="127.0.0.1", port=4000, debug=True)

