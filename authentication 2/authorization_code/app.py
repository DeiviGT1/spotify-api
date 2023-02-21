from flask import Flask, request, redirect, session, url_for, render_template
import requests
from flask_cors import CORS
import random
import string
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

app = Flask(__name__, template_folder="public")

client_id = '4e90e934295b4cb984d8ac90deab6d69' 
client_secret = '43f77b42f24f4ac4bb75552326377c5d'
redirect_uri = 'http://localhost:8000/callback'
stateKey = 'user-read-currently-playing'

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

@app.route('/login')
def login():
  #Acá ingresamos a la página de spotify para que el usuario se loguee
  state = generate_random_string(16)
  session[stateKey] = state
  scope = 'user-read-private user-read-email'
  #Redirigimos la pagina al callback
  return redirect('https://accounts.spotify.com/authorize?response_type=code&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&state=' + state)

@app.route('/callback')
def callback():
  code = request.args.get('code')
  state = request.args.get('state')
  stored_state = session[stateKey]
  
  return [code, state, stored_state]
  

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.run(host="localhost", port=8000, debug=True)

