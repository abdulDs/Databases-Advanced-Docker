import urllib.request
from bs4 import BeautifulSoup
import time
import pandas
from pymongo import MongoClient
import redis
import sys
import json


redis = redis.Redis(host='redis', port=6379)
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

    return pandas.DataFrame(list (zip(hashList,timeList,BTCamountList,amount)),
                        columns = ["Hash", "Time", "Amount (BTC)", "Amount (USD)"])



    ## caching the data into redis meomory and delet it after 60 se
while True:
    redis.set('key',scrapes_BTC_Data().to_json())
    redis.expire('key',60)
    time.sleep(63)
