import requests
import base64
import urllib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response, status

redirect_uri = 'http://localhost:4000/callback'
scope = "user-read-recently-played user-read-email"
token_url = 'https://accounts.spotify.com/api/token'
client_id='4e90e934295b4cb984d8ac90deab6d69'
client_secret='43f77b42f24f4ac4bb75552326377c5d'

def get_token(client_id, client_secret):
  client_str = f'{client_id}:{client_secret}'
  client_encode = base64.b64encode(client_str.encode("utf-8"))  # Codificado en Bytes
  client_encode = str(client_encode, "utf-8") 

  params = {'grant_type': 'client_credentials', 'scope': scope}
  headers = {'Authorization': f'Basic {client_encode}'}

  r = requests.post(token_url, data=params, headers=headers)
  token  = r.json()["access_token"]
  return token

api_token = get_token(client_id, client_secret)
header = {'Authorization': f'Bearer {api_token}'}

app = FastAPI()
templates = Jinja2Templates(directory="public")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login():
  #Redirigimos la pagina al callback
  return RedirectResponse(f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={scope}&scope={scope}')

@app.get("/callback")
def callback():
  return RedirectResponse('/user_id')

@app.get("/user_id")
def user_id():
  url = f"https://api.spotify.com/v1/me"
  r = requests.get(f'{url}', headers=header)
  return str(r)


@app.get("/recently_played/{user_id}")
def recently_played(user_id: str):
  url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
  r = requests.get(f'{url}', headers=header)
  return str(r)



# @app.route('/recently_played')
# def recently_played():
#   user_id = 
#   url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
#   r = requests.get(f'{url}', headers=header)
#   return str(r.status_code)

# r = requests.get(f'{url}', headers=header)
# print(r.json())
