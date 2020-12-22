from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
import urllib.parse
import redis
import pyarrow as pa


def scrape_cach():
    redis = redis.Redis(host='redis', port=6379)
    # this program scrapes the data from the website

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

    df = pd.DataFrame(list(zip(hashList, timeList, BTCamountList, amount)),
                      columns=["Hash", "Time", "Amount (BTC)", "Amount (USD)"])

    # cache the data
    # caching the data into redis meomory and delet it after 60 sec
    # undrerstand this ????
    context = pa.default_serialization_context()
    redis.set('key', context.serialize(df).to_buffer().to_pybytes())
    redis.expire('key', 60)


while (true):
    scrape_cach()
    time.sleep(60)
