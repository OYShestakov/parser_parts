# from selenium import webdriver
import time
from fake_useragent import UserAgent
from seleniumwire import webdriver

# url = "https://www.youtube.com/"

user_agent_list = [
    "hello_world",
    "best_of_the_best",
    "python_today"
]
ua = UserAgent()
options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={random.choice(user_agent_list)}")
options.add_argument(f"user-agent={ua.random}")

options.add_argument("--proxy-server=138.128.91.65:8000")


driver = webdriver.Chrome(executable_path="/Users/olegsestakov/Python/parser/chromedriver/chromedriver",
                          options=options
                          )

try:
    # driver.get(url="https://whatismybrowser.com/detect/what-is-my-user-agent")
    # time.sleep(5)
    driver.get("https//2ip.ru")
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
