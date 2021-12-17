import sqlite3

import requests

def refreshDataCandle(pair, Interval):
  r = requests.get("https://api.binance.com/api/v3/klines", params=dict(symbol=pair, interval= Interval))
  results = r.json()
  return(results[-1])

données = refreshDataCandle("BTCBUSD", "5m")

print(données[0])
print(données[2])
print(données[3])
print(données[1])
print(données[4])
print(données[5])


conn = sqlite3.connect('myDB.db')
cur = conn.cursor()
req = "insert into ApiBinance20211210(date, high, low, open, close, volume) values (?,?,?,?,?,?)"
values = (données[0],données[2],données[3],données[1],données[4],données[5])
cur.execute(req, values)
conn.commit()
conn.close