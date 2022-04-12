import json
import os.path
import time
import numpy as np
import requests
from bs4 import BeautifulSoup

url = "https://agroserver.ru/company/zapasnye-chasti-dlya-traktorov/"
def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0'
    }

    company_urls = []
    iteration_count = 7
    print(f"Всего итераций {iteration_count}")

    # Код запроса закоментирован сразу после создания файла с html.
    for item in range(1, 8):
        req = requests.get(url + f"p{item}.htm", headers=headers)

        folder_name = f"data/data_{item}"

        if os.path.exists(folder_name):
            print("Папка уже существует")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/company_{item}.html", "w") as file:
                file.write(req.text)

        # Открываем файл на чтение и передаем его в переменную.
        with open(f"{folder_name}/company_{item}.html") as file:
            src = file.read()

        # Создаем объект супа и забираем из класса все данные, которые мне нужны.
        soup = BeautifulSoup(src, "lxml")
        all_user_number = soup.find_all('div', class_="tovar")

        # Создаем цикл, бежим по списку и забираем ссылки, добавляем часть ссылки.
        for item in all_user_number:
            company_url = 'https://agroserver.ru' + item.find('div', class_="th").find('a').get('href') + 'contacts/?sm=1'
            company_name = item.find('div', class_="th").find('a').get('href')
            try:
                company_description = item.find("div", class_="text").text
            except Exception:
                company_description = "Описание отсутствует"
            company_urls.append(company_url)
        company_data_list = []
        for company_url in company_urls:
            req = requests.get(company_url, headers=headers)
            company_name = 'user_' + url.split('/')[2]
            with open(f"{folder_name}/{company_name}.html", "w") as file:
                file.write(req.text)

            with open(f"{folder_name}/{company_name}.html") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")

            try:
                company_inn = soup.find("td", class_="name").find("h1").findNext("div").text.split(',')[0].split(':')[1].strip()
            except Exception:
                company_inn = "Отсутствует"

            try:
                company_ogrn = soup.find("td", class_="name").find("h1").findNext("div").text.split(',')[1].split('\n')[0].split(':')[1].strip()
            except Exception:
                company_ogrn = "Отсутствует"

            company_data = soup.find("div", class_="rblock").find_all("span")
            company_site = soup.find("div", class_="rblock").find("a").get("href")
            if company_site[0] == '/':
                company_site = 'Отсутствует'
            company_face = company_data[0].text
            company_city = company_data[1].text
            company_phone = company_data[2].text
            company_data_list.append(
                {
                    "Название компании": company_name,
                    "Описание компании": company_description.strip(),
                    "ИНН": company_inn,
                    "ОГРН": company_ogrn,
                    "Контактное лицо": company_face,
                    "Город": company_city,
                    "Телефон": company_phone,
                    "Сайт": company_site
                }
            )
            iteration_count -= 1
            print(f"Осталось итераций №{iteration_count}")
            if iteration_count == 0:
                print("Сбор данных завершен")
            time.sleep((30 - 5) * np.random.random() + 5)
            with open("data/company_data.json", "a", encoding="utf-8") as file:
                json.dump(company_data_list, file, indent=4, ensure_ascii=False)


    # for company_card_url in company_cards[0:1]:
    #     req = requests.get(company_card_url, headers)
    #
    #     with open(f"Parser AgroServer/data/card_{company_name}.html", "w") as file:
    #         file.write(req.text)
    #
    #     with open(f"Parser AgroServer/data/card_{company_name}.html") as file:
    #         src = file.read()
    #
    #     soup = BeautifulSoup(src, "lxml")
    #     company_card = soup.find("div", class_="center").find_all("td")
    #     company_address = company_card[5].text
    #     print(company_address)


get_data(url)


