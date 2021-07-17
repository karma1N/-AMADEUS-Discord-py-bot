import requests
import json
from itertools import cycle
from events import version


response = requests.get("https://data.gateapi.io/api2/1/ticker/BTC_USDT")
ticket = json.loads(response.text)
BTCPRICE = ticket['last']

response = requests.get("https://data.gateapi.io/api2/1/ticker/ETH_USDT")
ticket = json.loads(response.text)
ETHPRICE = ticket['last']

status = cycle([f'BTC @ ${BTCPRICE}', f'ETH @  ${ETHPRICE}', f'.help | {version}'])
