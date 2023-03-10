from pymongo import MongoClient
from bson import json_util
import pandas as pd
from statistics import mean
from collections import defaultdict
import json

# client = MongoClient("ac-uhdra74-shard-00-01.tefpveq.mongodb.net:27017")
client = MongoClient('mongodb://localhost:27017/')
db = client['songs']
collection = db['songs']

user_id = "317ucfcdwpjhmasybsnbqc2j53jy"

def read_mongo(query={}, projection=None):
    """ Read from Mongo and return data in JSON format """
    # Make a query to the specific DB and Collection
    cursor = collection.find(query, projection)
    data = list(cursor)
    # Convert list of documents to JSON string
    json_data = json.dumps(data, default=json_util.default)
    return json_data

def delete_all_documents(query={}):
    """ Delete all documents from a MongoDB collection """
    # Delete all documents from the specified collection
    result = collection.delete_many(query)
    return result.deleted_count

def analyze_average_popularity_per_album():
  data = read_mongo(projection={'info.popularity': 1, 'info.playlist_name': 1, '_id': 0})
  data = json.loads(data)
  data = [x['info'] for x in data]
  result = defaultdict(list)

  for item in data:
      result[item['playlist_name']].append(item['popularity'])

  final_result = [{'playlist_name': k, 'average_popularity': sum(v)/len(v)} for k,v in result.items()]
  return final_result

  # df = pd.DataFrame(converted)
  # df = df.groupby('playlist_name').mean()
  # # df = pd.DataFrame([x['info'] for x in data])
  # return df
