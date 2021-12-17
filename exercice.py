import requests
import pandas as pd
import sqlite3

import time
import json
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode

def listAsset():
    r = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    results = r.json()
    for s in results['symbols']:
        print(s['symbol'])



def getDepth(SYMBOLE,INFO):
  r = requests.get("https://api.binance.com/api/v3/depth", params=dict(symbol=SYMBOLE))
  results = r.json()
  frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"], dtype=float) for side in [INFO]}
  return(frames)


def getOrderBook(SYMBOLE):
    limite = 50
    r=requests.get("https://api.binance.com/api/v3/depth" + "?symbol=" + SYMBOLE +"&limit=" + str(limite))
    return (r.json()['asks'],r.json()['bids'])

def refreshDataCandle(pair, Interval):
    r = requests.get("https://api.binance.com/api/v3/klines", params=dict(symbol=pair, interval= Interval))
    results = r.json()
    print(results)

    print("hight " + results[-1][2])
    print("low " + results[-1][3])
    print("open " + results[-1][1])
    print("close " + results[-1][4])
    print("volume " + results[-1][5])

    return(results)


def initDB():
    conn = sqlite3.connect('myDB.db')
    cur = conn.cursor()
    req = "create table ApiBinance20211210(Id integer primary key, date int, high real, low real, open real, close real, volume real)"
    cur.execute(req)
    conn.commit()
    conn.close
    return('succes')

def candleModify():
    conn = sqlite3.connect('myDB.db')
    cur = conn.cursor()
    req = "insert into ApiBinance20211210(date, high, low, open, close, volume) values (?,?,?,?,?,?)"
    données = refreshDataCandle("BTCUSDT", "5m")
    values = (données[0],données[2],données[3],données[1],données[4],données[5])
    cur.execute(req, values)
    conn.commit()
    conn.close
    return('succes')
    

API_KEY = 'use your API_KEY'
SECRET_KEY = 'use your SECRET_KEY'
BASE_URL = 'https://api.binance.com/'
PATH = 'api/v3/order/test'


headers = {
    'Content-Type': 'application/json',
    'X-MBX-APIKEY': API_KEY
}
def createOrder(api_key, secret_key, direction, price, amount, pair, orderType):
  timestamp = int(time.time() * 1000)
  params = {
      'symbol': pair, 
      'side':direction, 
      'price': price,
      'quoteOrderQty': amount,
      'type': orderType
  }
  query_string = urlencode(params)
  params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

  url = BASE_URL+PATH
  r = requests.post(url, headers=headers, params=params)
  print(r)
  if r.status_code == 200:
      data = r.json()
      print(json.dumps(data, indent=2))
      #return data
données = createOrder(API_KEY,SECRET_KEY,"SELL","500.0","0.1","ETHUSDT","LIMIT")
print(données)

def cancelOrder(symbol,orderId):
    secret = SECRET_KEY
    timestamp = requests.get(BASE_URL + "/api/v3/time").json()["serverTime"]
    query_string = "symbol="+symbol+"&orderId="+orderId+"&timestamp="+str(timestamp)
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': API_KEY
    }
    r=requests.delete(BASE_URL+"/api/v3/order?symbol="+symbol+"&orderId="+orderId+"&timestamp="+str(timestamp)+"&signature="+signature,headers=headers)
    print(r.text)




if __name__ == '__main__':
    #print(listAsset())
    #print(getDepth("BTCBUSD","bids"))
    #print(getDepth("BTCBUSD","asks"))
    #print(getOrderBook("BTCBUSD"))
    #print(refreshDataCandle("BTCUSDT", "5m"))
    #print(initDB())
    #print(candleModify())