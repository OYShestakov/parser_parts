import requests
from bs4 import BeautifulSoup
import re
import json

# url = 'https://agroserver.ru/company/zapasnye-chasti-dlya-traktorov/'

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0'
}

# req = requests.get(url, headers=headers)
# src = req.text

# with open('index.html', 'w') as file:
#     file.write(src)

# with open('index.html') as file:
#     src = file.read()

# soup = BeautifulSoup(src, 'lxml')
# user_number = soup.find_all(class_ = 'th')

# all_user_number_dict = {}
# for item in user_number:
#     item_text = item.text
#     item_href = 'https://agroserver.ru' + item.find('a').get('href') + 'contacts/?sm=1'.strip()    
#     all_user_number_dict[item_text] = item_href

# with open('all_user_number_dict.json', 'w') as file:
#     json.dump(all_user_number_dict, file, indent=4, ensure_ascii=False)

with open('all_user_number_dict.json') as file:
    all_user_number = json.load(file)

count = 0
for category_name, category_href in all_user_number.items():
        if count == 0:
            rep = [',', ' ', '-']
            for item in rep:
                if item in category_name:
                    category_name = category_name.replace(item, '_')

            req = requests.get(url = category_href, headers=headers)
            src = req.text

            with open(f"data/{count}_{category_name}.html", "w") as file:
                file.write(src)

            count += 1
