import requests
from bs4 import BeautifulSoup
import os

# url = ["http://rusagroset.ru/catalog/gruzovye_avto/", "http://rusagroset.ru/catalog/zil/"]
# headers = {
#     "Accept": "*/*",
#     "Bx-ajax": "true",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
# }
#
# for item in url:
#     req = requests.get(url=item, headers=headers)
#     src = req.text
#     soup = BeautifulSoup(src, "lxml")
#     try:
#         pagenets = int(soup.find("div", class_="bx-pagination-container").find_all("li")[-2].text)
#         print(pagenets)
#     except:
#         print("No pagenets")
#
#     for item in range(1, pagenets + 1):
#         url = f"{url}[item]{item}"
#         print(url)
# url = "http://rusagroset.ru/catalog/gruzovye_avto/"
# name_html = url.split("/")[-2]
# print(name_html)

fds = sorted(os.listdir('data/html'))
print(fds)