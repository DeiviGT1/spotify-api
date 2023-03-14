from pymongo import MongoClient
from bson import json_util
import pandas as pd
from statistics import mean
from collections import defaultdict
import json

usuario = "David"
contraseña = "David"

# Define la dirección IP del servidor de la base de datos y el nombre de la base de datos
direccion_ip_servidor = "songs.lohevn5.mongodb.net"
nombre_base_de_datos = "test"

# Crea una conexión con la base de datos de MongoDB
uri = f"mongodb+srv://{usuario}:{contraseña}@{direccion_ip_servidor}/{nombre_base_de_datos}" #?retryWrites=true&w=majority
client = MongoClient(uri)

# Selecciona la base de datos que deseas utilizar
db = client[nombre_base_de_datos]
collection = db['songs']

def read_mongo(query={}, projection=None):
    """ Read from Mongo and return data in JSON format """
    # Make a query to the specific DB and Collection
    cursor = collection.find(query, projection)
    data = list(cursor)
    # Convert list of documents to JSON string
    json_data = json.dumps(data, default=json_util.default)
    return json_data

def Mongo_Song_Data(songs_data):
    for item in songs_data:
        collection.insert_one({'info': item})

def delete_all_documents(query={}):
    """ Delete all documents from a MongoDB collection """
    # Delete all documents from the specified collection
    result = collection.delete_many(query)
    return result.deleted_count

def analyze_average_popularity_per_album(user_id):
  data = read_mongo(query={'info.user_id': user_id} ,projection={'info.popularity': 1, 'info.playlist_name': 1, '_id': 0})
  data = json.loads(data)
  data = [x['info'] for x in data]
  result = defaultdict(list)

  for item in data:
      result[item['playlist_name']].append(item['popularity'])

  final_result = [{'playlist_name': k, 'average_popularity': "{:.2f}".format(sum(v)/len(v))} for k,v in result.items()]
  return final_result
