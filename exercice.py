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
    return(results[1])


def initDB():
    conn = sqlite3.connect('myDB.db')
    cur = conn.cursor()
    req = "create table ApiBinance20211210(Id integer primary key, date int, high real, low real, open real, close real, volume real)"
    cur.execute(req)
    conn.commit()
    conn.close

def candleModify():
    conn = sqlite3.connect('myDB.db')
    cur = conn.cursor()
    req = "insert into ApiBinance20211210(date, high, low, open, close, volume) values (?,?,?,?,?,?)"
    données = refreshDataCandle("BTCUSDT", "5m")
    values = (données[0],données[2],données[3],données[1],données[4],données[5])
    cur.execute(req, values)
    conn.commit()
    conn.close


API_KEY = 'HfZyng5y8XJZAs37J9uV3bhwWGVODNWAmEoctEqe7MPnFaEKvaNo98SnXItl1n7s'
SECRET_KEY = 'uwPBFzyMuM2hg9PjwQV518AR3ULuu2ZsZftlinVckrRIEPSU7pwnwqJpLGJayEi5'
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






#print(listAsset())
#print(getDepth("BTCBUSD","bids"))
#print(getDepth("BTCBUSD","asks"))
#print(getOrderBook("BTCBUSD"))
print(refreshDataCandle("BTCBUSD","5m"))