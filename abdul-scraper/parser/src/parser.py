import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import redis
import pyarrow as pa


def get_insert():
    redis = redis.Redis(host='localhost', port=6379)
    context = pa.default_serialization_context()
    # git the cached data and sort the highest value
    topValue = context.deserialize(redis.get('key')).sort_values(
        by=['Amount (USD)'], ascending=False).head(1).iloc[0].to_dict()

    client = MongoClient('mongod', port=27017)
    # insert the top value in our mongodb
    db = client.largest_btc
    notebook = db.notebook
    notebook.insert_one(topValue)


while (true):
    get_insert()
    time.sleep(60)
