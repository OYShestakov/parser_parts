import json
import math
import random
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import csv

# url = "https://1belagro.com/catalog/"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

def get_urls(url):
    # req = requests.get(url, headers)
    # src = req.text
    #
    # with open("category.html", "w") as file:
    #     file.write(src)
    urls_category = []
    with open("category.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    urls_category_data = soup.find("div", class_="catalog-list sections").find_all("li")
    for item in urls_category_data:
        link = f"https://1belagro.com" + item.find("a").get("href")
        count_in_category = int(item.find("span").text[1: -1])
        count_in_category = math.ceil(count_in_category)
        urls_category.append(link)

    with open("category.json", "w") as file:
        json.dump(urls_category, file, indent=4, ensure_ascii=False)




def get_html():

    with open("category.json") as file:
        src = json.load(file)

    for item in src:
        category_name = item.split("/")[-2]
        req = requests.get(item, headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        try:
            count_in_category = int(soup.find(class_="catalog-elements-count").text.split(" ")[-2])
            count_in_category = math.ceil(count_in_category/20)
        except:
            continue
        if count_in_category == 1:

            with open(f"data/data_html/page_html_{category_name}_{count_in_category}.html", "w") as file:
                file.write(src)
            print(f"Файл создан без пагенации {category_name}")
            time.sleep(random.randrange(2, 8))
        else:
            for item in range(1, count_in_category + 1):
                url = f"https://1belagro.com/catalog/zapchasti-k-traktoram-i-gruzovym-auto/{category_name}/?PAGEN_1={item}"
                req = requests.get(url=url, headers=headers)
                src = req.text

                with open(f"data/data_html/page_html_{category_name}_{item}.html", "w") as file:
                    file.write(src)
                print(f"Создал файл в пагенации {category_name}_{item}")
                time.sleep(random.randrange(2, 8))


def get_parts():
    fds = sorted(os.listdir('data/data_html'))

    with open("data/data_csv/data_csv_belagro.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Наименование",
                "Наличие",
                "Цена"
            )
        )
    count_page = 831
    for page in fds:

        with open(f"data/data_html/{page}") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        try:
            project_data = soup.find_all("div", class_="catalog_list_detailed")
        except:
            print(f"Не нашел данных в файле {page}")
            continue
        for item in project_data[1:]:
            try:
                product_name = item.find("div", class_="info cf").find("a").text.strip()
            except:
                product_name = "Не указано"
            try:
                product_in_stock = item.find("div", class_="info cf").find("div", class_="geo").find("div", class_="text-quantity text-green").text.strip()
            except:
                product_in_stock = "Под заказ"
            try:
                product_price = item.find("div", class_="info cf").find("div", class_="price_wrap").find("div", class_="price").find("span", class_="current_price").text.strip()
            except:
                product_price = "0"
            with open("data/data_csv/data_csv_belagro.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product_name,
                        product_in_stock,
                        product_price
                    )
                )
        count_page -= 1
        print(f"Осталось обработать {count_page}/831")


def main():
    # get_urls(url)
    # get_html()
    get_parts()

if __name__ == '__main__':
    main()