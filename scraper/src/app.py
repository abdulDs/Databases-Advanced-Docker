from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import urllib.parse
import redis
import pyarrow as pa

redis = redis.Redis(host='redis', 6379)# expose it to the same port
# this program scrapes the data from the website


def scrape_cach():
    r = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions')
    soup = BeautifulSoup(r.text, 'lxml')

    hashList = []
    timeList = []
    BTCamountList = []
    USDamountList = []

    a = soup.findAll('div', {"class": "sc-1g6z4xm-0 arCxa"})
    for element in a:
        hashList.append(element.findAll(['span', 'a'])[1].text)
        timeList.append(element.findAll(['span', 'a', ])[3].text)
        BTCamountList.append(element.findAll(['span', 'a'])[5].text)
        USDamountList.append(element.findAll(['span', 'a', ])[7].text)

    stripedList = [s.strip('$')for s in USDamountList]
    amount = [float(s.replace(',', '')) for s in stripedList]

    scraped_BTC_Data = pd.DataFrame(list(zip(hashList, timeList, BTCamountList, amount)),
                                    columns=["Hash", "Time", "Amount (BTC)", "Amount (USD)"])

    # caching the data into redis meomory and delet it after 60 sec
    context = pa.default_serialization_context()
    redis.set('key', context.serialize(
        spd.scraped_BTC_Data).to_buffer().to_pybytes())
    redis.expire('key', 60)
    return context


while True:
    scrape_cach()
    time.sleep(60)
