import numpy as np
import pandas as pd
from pymongo import MongoClient
import urllib.parse
import redis
from app import *

# this code depands on the scraper so the scraper will insert the dat to redis and return to us data we will filter it and store to mongodb
topFromredis = scrape_cach().deserialize(redis.get('key')).sort_values(
    by=['Amount (USD)'], ascending=False).head(1).iloc[0].to_dict()

client = MongoClient(host='mongo', port=27017)  # expose to the same port
# insert the top value in our mongodb

db = client.largest_btc
notebook = db.notebook
notebook.insert_one(topFromredis)
