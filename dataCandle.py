import requests

def refreshDataCandle(pair, Interval):
  r = requests.get("https://api.binance.com/api/v3/klines", params=dict(symbol=pair, interval= Interval))
  results = r.json()
  print(results)
  return(results[1])

données = refreshDataCandle("BTCUSDT", "5m")

print(données)

print(données[0])
print("hight " + données[2])
print("low " + données[3])
print("open " + données[1])
print("close " + données[4])
print("volume " + données[5])