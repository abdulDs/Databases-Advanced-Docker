import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import urllib.parse
import redis
import pyarrow as pa
import sys

redis = redis.Redis(host='localhost', port=6379)
def scrapes_BTC_Data():
    r = urllib.request.urlopen('https://www.blockchain.com/btc/unconfirmed-transactions')
    soup = BeautifulSoup(r, 'html.parser')
    hashList=[]
    timeList=[]
    BTCamountList=[]
    USDamountList=[]

    a = soup.findAll('div', {"class":"sc-1g6z4xm-0 hXyplo"})
    for element in a:
        hashList.append(element.findAll(['span','a'])[1].text)
        timeList.append(element.findAll(['span','a',])[3].text)
        BTCamountList.append(element.findAll(['span','a'])[5].text)
        USDamountList.append(element.findAll(['span','a',])[7].text)

    stripedList = [s.strip('$')for s in USDamountList]
    amount = [float(s.replace(',','')) for s in stripedList]

    df = pd.DataFrame(list (zip(hashList,timeList,BTCamountList,amount)),
                        columns = ["Hash", "Time", "Amount (BTC)", "Amount (USD)"])


    ## caching the data into redis meomory and delet it after 60 sec
    context = pa.default_serialization_context()
    redis.set('key',context.serialize(df).to_buffer().to_pybytes())
    redis.expire('key',60)

while True:
    scrapes_BTC_Data()
    time.sleep(60)
