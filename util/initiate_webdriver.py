from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def initiate_driver():
    # options = Options()
    # options.headless = True
    # page_to_scrape = webdriver.Chrome(options=options)
    page_to_scrape = webdriver.Chrome()
    return page_to_scrape

# options = Options()
# options.headless = True
# page_to_scrape = webdriver.Chrome(options=options)