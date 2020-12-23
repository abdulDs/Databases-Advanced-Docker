import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import redis
import json


redis = redis.Redis(host='localhost', port=6379)
client = MongoClient('localhost', port=27017)
# insert the top value in our mongodb
def storeToMongodb():
    observations = pd.read_json(redis.get('key'))
    topObservation = observations.sort_values(by=['Amount (USD)'], ascending=False).head(1).iloc[0]
    db = client.largest_btc
    notebook = db.notebook
    print(topObservation)
    notebook.insert_one(topObservation.to_dict())

while True:
    storeToMongodb()
    time.sleep(63)
