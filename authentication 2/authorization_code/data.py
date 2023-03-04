import pandas as pd
from pymongo import MongoClient

def _connect_mongo(host, port, username, password, db):
  if username and password:
    mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
    conn = MongoClient(mongo_uri)
  else:
    conn = MongoClient(host, port)


  return conn[db]

def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True, projection = None):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query, projection)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
      return "No id"
        # del df['_id']

    return df

new_query = ({}, { "artist_0": 1, "popularity": 1, "_id": 0 })
x = read_mongo(db = "songs", collection= "songs", projection=['artist_0', 'popularity'])
x = read_mongo(db = "songs", collection= "songs", query={"artist_0": "Rels B"}, projection=['artist_0', 'popularity'])

# x = read_mongo(db = "songs", collection= "songs", query = {'popularity': {'$lt': 30}}, projection=['artist_0', 'popularity'])
# x = read_mongo(db = "songs", collection= "songs", query = new_query, projection=['artist_0', 'popularity'])
print(x)