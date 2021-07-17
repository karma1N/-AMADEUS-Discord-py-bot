import requests
import json
import shutil
import os
import time


def clear():
    os.remove("statusapi.json")
    time.sleep(1.5)
    shutil.copy("C:/Users/adrie/PycharmProjects/Amadeus/api/statusapi.json",
                "C:/Users/adrie/PycharmProjects/Amadeus/statusapi.json")
    time.sleep(5)
    refresh()


def refresh():
    with open('statusapi.json') as json_file:
        data = json.load(json_file)

        response = requests.get("https://data.gateapi.io/api2/1/ticker/btc_usdt")
        ticket = json.loads(response.text)

        price = ticket['last']

        api = {"BTCUSDT": price}

        data.append(api)

    with open('statusapi.json', 'w') as f:
        json.dump(data, f, indent=2)

    eth()


def eth():
    with open('statusapi.json') as json_file:
        data = json.load(json_file)

        response = requests.get("https://data.gateapi.io/api2/1/ticker/eth_usdt")
        ticket = json.loads(response.text)

        price = ticket['last']

        api = {"ETHUSDT": price}

        data.append(api)

    with open('statusapi.json', 'w') as f:
        json.dump(data, f, indent=2)

    xch()


def xch():
    with open('statusapi.json') as json_file:
        data = json.load(json_file)

        response = requests.get("https://data.gateapi.io/api2/1/ticker/xch_usdt")
        ticket = json.loads(response.text)

        price = ticket['last']

        api = {"CHIAUSDT": price}

        data.append(api)

    with open('statusapi.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    clear()
