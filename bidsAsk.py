import requests
import pandas as pd

def SymboleAskBid(SYMBOLE,INFO):
  r = requests.get("https://api.binance.com/api/v3/depth", params=dict(symbol=SYMBOLE))
  results = r.json()
  frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"], dtype=float) for side in [INFO]}
  print(frames)

SymboleAskBid("BTCBUSD","bids")
SymboleAskBid("BTCBUSD","asks")