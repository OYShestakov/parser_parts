import time
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from fake_headers import Headers
import os
import csv




url = "https://agrolider.ua/"

headers = Headers(headers=True).generate()


def get_category_urls(url=url):
    # options = webdriver.ChromeOptions()
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")
    # driver = webdriver.Chrome(executable_path="/Users/olegsestakov/Python/parser/chromedriver/chromedriver",
    #                           options=options
    #                           )
    #
    # try:
    #     driver.get(url=url)
    #     time.sleep(5)
    #     category_html = driver.page_source
    #     with open("category.html", "w") as file:
    #         file.write(category_html)
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     driver.close()
    #     driver.quit()

    with open("category.html") as file:
        src = file.read()
    collect_url_list = []
    soup = BeautifulSoup(src, "lxml")
    page_data = soup.find("div", class_="row imgcategory").find_all("div", class_="col-lg-3 col-md-3 col-sm-6 col-xs-12")
    for item in page_data:
        url = item.find("div", class_="image").find("a").get("href")
        collect_url_list.append(url)

    with open("collect_urls.json", "a") as file:
        json.dump(collect_url_list, file, indent=4, ensure_ascii=False)




def get_html():
    headers = Headers(headers=True).generate()

    with open("collect_urls.json") as file:
        src = json.load(file)

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="/Users/olegsestakov/Python/parser/Parser agrolider.ua/chromedriver",
                              options=options
                              )

    try:
        for item in src:
            driver.get(url=item)
            time.sleep(random.uniform(3, 6))
            category_name = item.split("/")[-2]
            category_link = item
            category_html = driver.page_source
            soup = BeautifulSoup(category_html, "lxml")
            pagenation_count = int(soup.find("div", class_="col-sm-6 text-right").text.split(" ")[-2])

            with open(f"data_category_html/category_{category_name}.html", "w") as file:
                file.write(category_html)

            print(f"Создал файл без пагенации - {category_name}")
            if pagenation_count > 1:
                for item in range(2, pagenation_count + 1):
                    url = f"{category_link}?page={item}"
                    driver.get(url=url)
                    time.sleep(random.uniform(3, 8))
                    category_html = driver.page_source

                    with open(f"data_category_html/category_{category_name}_{item}.html", "w") as file:
                        file.write(category_html)

                    print(f"Создал файл - {category_name}_{item}")

    except Exception as ex:
        print(f"Ошибка - {ex}\nОбрабатывал ссылку {item}")
    finally:
        driver.close()
        driver.quit()
        print("Работа завершена, браузер закрыт!")





def get_data_parts():
    fds = sorted(os.listdir('data_category_html'))

    with open("data_agrolider_ua.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Наименование",
                "Ссылка на товар",
                "Цена",
                "Ссылка на фото"
            )
        )
    page_count = 557
    collect_link_parts = []
    for page in fds:

        with open(f"data_category_html/{page}") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        parts_data = soup.find_all("div", class_="caption")
        if len(parts_data) > 1:
            for item in parts_data:

                try:
                    parts_link = item.find("div", class_="div_h4 fix-height").find("a").get("href").strip()
                except:
                    continue
                collect_link_parts.append(parts_link)
    print(len(collect_link_parts))

    with open("collect_link_parts.json", "a") as file:
        json.dump(collect_link_parts, file, indent=4, ensure_ascii=False)

        page_count -= 1
        print(page_count)









def main():
    # get_category_urls()
    # get_html()
    get_data_parts()


if __name__ == '__main__':
    main()