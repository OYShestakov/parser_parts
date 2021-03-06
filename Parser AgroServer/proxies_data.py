import os
import requests
import random
import pickle
from itertools import cycle
from requests_html import HTMLSession
from datetime import datetime


def get_random_proxy():

    now_time = datetime.now()

    if "proxies.pickle" in os.listdir("."):
        with open("proxies.pickle", "rb") as f:
            proxies_dump = pickle.load(f)
            dump_time = proxies_dump[1][1]["last_check"]
            proxy_list = proxies_dump[1]
            date_time_obj = datetime.strptime(dump_time, "%Y-%m-%d %H:%M:%S")
    else:
        dump_time = None

    if not dump_time or (now_time - date_time_obj).days > 1:

        json_url = "http://api.best-proxies.ru/proxylist.json"
        query_params = {
            "key": "api_key",
            "limit": 100,
            "type": "http"
        }

        with HTMLSession() as session:
            response = session.get(json_url, params=query_params)

        proxy_list = response.json()

        with open("proxies.pickle", "wb") as f:

            pickle.dump((dump_time, proxy_list), f)

    random_proxy = random.choice(proxy_list)

    proxies = {
        "http": f"http://{random_proxy['ip']}:{random_proxy['port']}"
    }

    return proxies

if __name__ == '__main__':
    data = get_random_proxy()

