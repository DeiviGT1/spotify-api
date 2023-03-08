
import requests 
import json 
import requests 
import base64 
import urllib 
import urllib.parse 
from flask import request 
CLIENT_ID = "4e90e934295b4cb984d8ac90deab6d69" 
CLIENT_SECRET = "43f77b42f24f4ac4bb75552326377c5d" 
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize" 
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token" 
SPOTIFY_API_BASE_URL = "https://api.spotify.com" 
API_VERSION = "v1" 
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{API_VERSION}'

# Server-side Parameters 
CLIENT_SIDE_URL = "http://localhost" 
PORT = 4000 
REDIRECT_URI = f"{CLIENT_SIDE_URL}:{PORT}/callback" 
SCOPE = "user-library-read" 
STATE = "" 
SHOW_DIALOG_bool = True 
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower() 

def user_Authorization(): 
  auth_token = request.args['code'] 
  code_payload = { "grant_type": "authorization_code", "code": str(auth_token), "redirect_uri": REDIRECT_URI } 
  client_str = f'{CLIENT_ID}:{CLIENT_SECRET}' 
  client_encode = base64.b64encode(client_str.encode("utf-8")) 
  
  # Codificado en Bytes 
  client_encode = str(client_encode, "utf-8") 
  headers = {"Authorization": f"Basic {client_encode}"} 
  post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers) 
  
  # Tokens are Returned to Application 
  response_data = json.loads(post_request.text) 
  access_token = response_data["access_token"] 
  refresh_token = response_data["refresh_token"] 
  token_type = response_data["token_type"] 
  expires_in = response_data["expires_in"] 
  
  # Use the access token to access Spotify API 
  authorization_header = {"Authorization":f"Bearer {access_token}"} 
  return authorization_header 
  
authorization_header = user_Authorization()
