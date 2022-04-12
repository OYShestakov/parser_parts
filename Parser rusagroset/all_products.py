import os
from bs4 import BeautifulSoup
import requests
import lxml
import time
import csv
import json
import random
from fake_headers import Headers
from numpy.core.defchararray import upper

url = "http://rusagroset.ru/catalog/zapchasti_dlya_traktorov_i_gruzovykh_avtomobiley/"
headers = Headers(headers=True).generate()
urls_data_list = []
product_data_list = []
clear_urls = []

def get_data_url(url, headers):
    req = requests.get(url, headers)
    with open("index_url.html", "w") as file:
        file.write(req.text)
    with open("index_url.html") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    # urls_data = soup.find_nexd("div", class_="c_wrapper27").find_next("ul", id="black").find_all("li")
    urls_data = soup.find(id="bx_1847241719_177").find("ul").find_all("li")
    for item in urls_data:
        url = f"http://rusagroset.ru" + item.find("a").get("href")
        urls_data_list.append(url)

    with open("all_urls.json", "a", encoding="utf-8") as file:
        json.dump(urls_data_list, file, indent=4, ensure_ascii=False)


def get_html_data():
    with open('all_urls.json') as file:
        url_category = json.load(file)

    for item in url_category:
        urls_item = item
        req = requests.get(item, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        name_html = item.split("/")[-2]
        time.sleep(random.randrange(2, 4))

        try:
            project_data = soup.find_all("div", class_="container_add_pos")
        except:
            print(f"{urls_item} товаров не обнаружено")
            continue

        try:
            pagen = int(soup.find("div", class_="bx-pagination-container").find_all("li")[-2].text)
            for item_html in range(1, pagen + 1):
                url = f"{urls_item}?PAGEN_1={item_html}"
                name_html = urls_item.split("/")[-2]
                time.sleep(random.randrange(2, 4))
                req = requests.get(url=url, headers=headers)
                src = req.text
                soup = BeautifulSoup(src, "lxml")

                with open(f"data/html/{name_html}{item_html}.html", "w") as file:
                    file.write(src)
                print(f"{name_html}_{item_html} - создан в цикле с пагенцией")
        except Exception as ex:
            print(ex)
            if len(project_data) > 0:
                with open(f"data/html/{name_html}.html", "w") as file:
                    file.write(src)
                print(f"{name_html} - создан в except")
            else:
                continue



def collect_data():
    fds = sorted(os.listdir('data/html'))
    with open("data/data_csv/data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Категория",
                "Наименование",
                "Количество в наличии",
                "Цена",
                "Ссылка на фото"
            )
        )
    for page in fds:
        with open(f"data/html/{page}") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        project_data = soup.find_all("div", class_="container_add_pos")
        category_name = soup.find("div", class_=r"\article_title").text.strip()
        print(f"Работаю с файлом: {page}")

        for item in project_data:
            try:
                product_name = item.find("div", class_="parts_title").find("span").text.replace("-", "")
            except Exception:
                continue
            try:
                product_available = item.find("div", class_="parts_rest").find_all("span")[1].text
            except Exception:
                product_available = "Наличие не указано"
            try:
                product_price = item.find("div", class_="parts_price").find("span").text
            except Exception:
                product_price = "Цена не указана"
            try:
                parts_photo = f"https://rusagroset.ru" + item.find("img").get("src")
            except Exception as ex:
                print(ex)
            product_data_list.append(
                {
                    "Категория": category_name,
                    "Название": product_name,
                    "В наличии": product_available,
                    "Цена": product_price,
                    "Ссылка на фото": parts_photo
                }
            )

            with open("data/data_csv/data.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        category_name,
                        product_name,
                        product_available,
                        product_price,
                        parts_photo
                    )
                )
            # with open("data/data_csv/data.json", "a") as file:
            #     json.dump(product_data_list, file, indent=4, ensure_ascii=False)



# get_data_url(url, headers)
# get_html_data()
collect_data()
