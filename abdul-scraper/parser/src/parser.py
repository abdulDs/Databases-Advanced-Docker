import time
import pandas
from pymongo import MongoClient
import redis
import json
import sys

redis = redis.Redis('redis', port=6379)
client = MongoClient("mongodb://mongo")
# insert the top value in our mongodb

db = client.toptop
notebook = db.notebook
def topValue():
    key = redis.get('key')
    observations = pandas.read_json(key)
    topObservation = observations.sort_values(by=['Amount (USD)'], ascending=False).head(1).iloc[0]
    return topObservation


while True:
    time.sleep(20)
    x = topValue()
    if x is not None:
        while True:
            top = topValue()
            notebook.insert_one(top.to_dict())
            time.sleep(60)
