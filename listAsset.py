import requests
import pandas as pd

r = requests.get("https://api.binance.com/api/v3/exchangeInfo")

results = r.json()

for s in results['symbols']:
    print(s['symbol'])