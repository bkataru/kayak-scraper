import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent


def create_scraper():
    options = Options()
    ua = UserAgent()

    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    return driver

def crawl():
    driver = create_scraper()
    print("Selenium driver initialized")
    
    driver.get(
        'https://www.kayak.co.in/flights/BOM-DEL/2024-03-25?fs=fdDir=true;stops=~0&sort=bestflight_a#default'
    )
    print("Accessed page, waiting 20s")
    time.sleep(20)
    
    # times = 1
    # while True:
    #     try:
    #         element = driver.find_element(By.CLASS_NAME, 'show-more-button')
    #         element.click()
    #         print(f"Clicked show more {times} times, waiting 5s")
    #         times += 1
    #         time.sleep(5)
    #     except NoSuchElementException:
    #         print("Element not found.")
    #         break
    
    for i in range(4):
        driver.find_element(By.CLASS_NAME, 'show-more-button').click()
        print(f"Clicked show more {i + 1} times, waiting 5s")
        time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    print("Obtained page source")
    
    with open('index.html', 'w') as f:
        f.write(soup.prettify())
        print("Dumped page source")
    