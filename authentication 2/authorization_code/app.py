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
scope = 'user-read-email'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login/')
def login():
  #Acá ingresamos a la página de spotify para que el usuario se loguee
  #Redirigimos la pagina al callback
  return redirect(f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}')

@app.route('/callback')
def callback():
  
  return redirect('/recently_played')

@app.route('/recently_played')
def recently_played():
  access_token = get_token(client_id, client_secret, scope=scope)

  # Codificamos el cliente
  endpoint = "https://api.spotify.com/v1/me"
  headers = {'Authorization': f'Bearer {access_token}'}
  
  new_response = requests.get(endpoint, headers=headers)
  return str(new_response.status_code)

  if response.status_code != 200:
    return make_response(f'Error: Failed to get top tracks. Status code: {response.status_code}', 500)


  return str(response.status_code)
  #Obtenemos los datos del usuario 
    
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
  return str(api_key)

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=2000, debug=True)


# playlist_endpoint = "https://api.spotify.com/v1/playlists/0zUlV7QuNqu31SCTlGRo9X"
# headers = {"Authorization": f"Bearer {api_key}"}

# response = requests.get(playlist_endpoint, headers=headers)
# json_response = json.loads(response.content)