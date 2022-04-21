from bs4 import BeautifulSoup
import requests
import lxml
import time
import random


for item in range(1, 13):
    url = f"https://pythonist.ru/category/tests/page/{item}"
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    # name_html = item.split("/")[-2]
    time.sleep(random.randrange(2, 4))

    try:
        project_data = soup.find_all("h2", class_="entry-title")
        for data in project_data:
            url_test = data.find('a').get('href')
            text_test = data.find('a').text
            print(text_test)



    except:
        print(f"{url} тестов не обнаружено")
        continue

