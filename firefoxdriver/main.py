from selenium import webdriver
import time
from fake_useragent import UserAgent

url = "https://www.youtube.com/"

useragent = UserAgent()
options = webdriver.FirefoxOptions()

options.set_preference("general.useragent.override", useragent.random)

driver = webdriver.Firefox(
    executable_path="/Users/olegsestakov/Python/parser/firefoxdriver/geckodriver",
    options=options
)

try:
    driver.get(url="https://whatismybrowser.com/detect/what-is-my-user-agent")
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()