import requests
import json
import requests
import base64
from flask import Flask, render_template, session, redirect, request, make_response
import urllib

app = Flask(__name__, template_folder="public")

client_id = "4e90e934295b4cb984d8ac90deab6d69"
client_secret = "43f77b42f24f4ac4bb75552326377c5d"
redirect_uri = 'http://127.0.0.1:2000/callback'
scope = 'user-read-recently-played'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login')
def login():
  #Acá ingresamos a la página de spotify para que el usuario se loguee
  #Redirigimos la pagina al callback
  return redirect(f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}')

@app.route('/callback')
def callback():
    # Codificamos el cliente
    access_token = get_token(client_id, client_secret, scope="user-read-recently-played")
    response = make_response('Token generated successfully')
    response.headers['access_token'] = access_token
    return redirect(f'/recently-played')

@app.route('/recently-played')
def recently_played():
  # Codificamos el cliente
  endpoint = "https://api.spotify.com/v1/me/player/recently-played"
  headers = request.headers.get('access_token')
  return str(headers)
  #Obtenemos los datos del usuario
  response = requests.get(endpoint, headers=headers)
  json_response = json.loads(response.content)

  return json_response    

    

def get_token(client_id, client_secret, scope = None):
  #Codificamos el cliente 
  client_creds = f"{client_id}:{client_secret}"
  client_creds_b64 = base64.b64encode(client_creds.encode())
  #Ruta del endpoint de la API de spotify para obtenerlo
  token_endpoint = "https://accounts.spotify.com/api/token"
  #paramertros para el token y credenciales de la solicitud
  token_data = {
    "grant_type": "client_credentials",
    "scope" : f"{scope}"
}
  token_headers = {
      "Authorization": f"Basic {client_creds_b64.decode()}"
  }
  # Solicitud del toke y respuesta en JSON
  token_response = requests.post(token_endpoint, data=token_data, headers=token_headers)
  token_json_response = token_response.json()
  api_key = token_json_response['access_token']
  return api_key

def get_recently_played(api_key):
  endpoint = "https://api.spotify.com/v1/me/player/recently-played"
  headers = {"Authorization": f"Bearer {api_key}"}

  response = requests.get(endpoint, headers=headers)
  json_response = json.loads(response.content)

  return json_response

def get_recently_played_tracks(access_token):
    # Hacer una solicitud a la API de Spotify para obtener el historial de reproducciones del usuario
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=10"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)

    # Procesar los datos de la respuesta
    if response.status_code == 200:
        tracks = []
        data = json.loads(response.content)
        for item in data["items"]:
            track = item["track"]
            tracks.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "date": item["played_at"]
            })
        return tracks
    else:
        print("Error al obtener los datos del usuario:", response.status_code)
        return None

api_key = get_token(client_id, client_secret, scope="user-read-recently-played")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=2000, debug=True)


# playlist_endpoint = "https://api.spotify.com/v1/playlists/0zUlV7QuNqu31SCTlGRo9X"
# headers = {"Authorization": f"Bearer {api_key}"}

# response = requests.get(playlist_endpoint, headers=headers)
# json_response = json.loads(response.content)