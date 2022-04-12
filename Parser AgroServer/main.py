import requests
from bs4 import BeautifulSoup
import json
import time
import random
import csv
import os
from fake_headers import Headers

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

proxies = {
    "http": "http://88.198.24.108:3128",
    "http": "http://176.9.119.170:3128",
    "http": "http://50.206.25.109:80",
    "http": "http://50.206.25.106:80",
    "http": "http://85.26.146.169:80",
    "http": "http://68.188.59.198:80",
    "http": "http://68.185.57.66:80",
    "http": "http://50.206.25.107:80",
    "http": "http://50.206.25.111:80",
    "http": "http://50.206.25.110:80"
}

def get_company_urls():
    # for item in range(1, 8):
    #     url = f"https://agroserver.ru/company/zapasnye-chasti-dlya-traktorov/p{item}.htm"
    #     req = requests.get(url=url, headers=headers)
    #     src = req.text
    #
    #     with open(f"data/page_html_{item}", "a") as file:
    #         file.write(src)
    #     time.sleep(random.randrange(5, 10))
    fds = sorted(os.listdir('data'))
    company_link_list = []
    for page in fds:

        with open(f"data/{page}") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        try:
            company_urls = soup.find("div", class_="b_list_full").find_all("div", class_="wrapper")
            print(company_urls)
        except:
            print(f"Не нашел информации в файле {page}")
            continue
        for item in company_urls:
            company_link = f"https://agroserver.ru" + item.find("div", class_="th").find("a").get("href")
            company_link_list.append(company_link)
    print(len(company_link_list))
    with open("company_link.json", "w") as file:
        json.dump(company_link_list, file, indent=4, ensure_ascii=False)


def get_company_html():
    headers = Headers(headers=True).generate()

    with open("company_link.json") as file:
        src = json.load(file)

    for item in src:
        req = requests.get(url=item, headers=headers, proxies=proxies)
        src = req.text
        status = req.status_code
        item_link = item
        number_company = item.split("/")[-2]
        print(f"{item} - {status}")
        time.sleep(random.uniform(3, 8))
        if status == 200:
            with open(f"data_html_company/company_html_data_{number_company}.html", "w") as file:
                file.write(src)
            obj = json.load(open("company_link.json"))
            for i in range(len(obj)):
                if obj[i] == f"{item_link}":
                    obj.pop(i)
                    break
        else:
            print(status)
            break




def get_company_data():
    pass


def main():
    # get_company_urls()
    get_company_html()
    get_company_data()


if __name__ == '__main__':
    main()
