import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import redis
import pyarrow as pa
import redis

context = pa.default_serialization_context()
redis = redis.Redis(host='localhost', port=6379)
client = MongoClient('localhost', port=27017)
# insert the top value in our mongodb
def storeToMongodb():
    observations =  redis.get('key')
    topObservation = context.deserialize(observations).sort_values(by=['Amount (USD)'], ascending=False).head(1).iloc[0].to_dict()
    db = client.largest_btc
    notebook = db.notebook
    print(topObservation)
    notebook.insert_one(topObservation)

while True:
    storeToMongodb()

    time.sleep(63)
