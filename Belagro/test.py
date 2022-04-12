import math
from fake_headers import Headers
import string
import re

# count_in_category = math.ceil(4986/100)
# print(count_in_category)
# a = "Всего в разделе  4986 товаров:"
# a = int(a.split(" ")[-2])
# print(a/100)
# a = math.ceil(a/100)
# print(a)

# a = "Показано с 1 по 9 из 9 (всего 1 страниц)"
# a = a.split(" ")[-2]
# print(a)

# headers = Headers(headers=True).generate()

# proxy = get_random_proxy()
# print(f"Делаю запрос через прокси {proxy}")


article = input("Введите артикулы:")
article = re.split('[., ]+', article)
print(article)