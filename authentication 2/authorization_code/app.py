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

from flask import Flask, render_template, request, make_response, redirect
import requests

# Página para obtener el token de acceso
@app.route('/login')
def get_token():
    # Obtener el código de autorización proporcionado por Spotify
    authorization_code = request.args.get('code')
    return str(authorization_code)

    # Intercambiar el código de autorización por un token de acceso
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # Obtener el token de acceso de la respuesta
    auth_response_data = auth_response.json()
    return auth_response_data
    access_token = auth_response_data['access_token']

    # Devolver el token de acceso en la respuesta HTTP
    response = make_response('Token generated successfully')
    response.headers['access_token'] = access_token

    # Redirigir al usuario a la página de uso del token
    return redirect('/use_token')

# Página para usar el token de acceso
@app.route('/use_token')
def use_token():
    # Obtener el token de acceso del encabezado HTTP de la solicitud entrante
    access_token = request.headers.get('access_token')

    # Usar el token de acceso para hacer solicitudes a la API de Spotify
    response = requests.get('https://api.spotify.com/v1/me', headers={
        'Authorization': 'Bearer ' + access_token
    })

    # Obtener los datos de usuario de la respuesta
    user_data = response.json()

    # Devolver los datos de usuario en la página web
    return user_data

if __name__ == "__main__":
    app.run(debug=True, port=2000)
