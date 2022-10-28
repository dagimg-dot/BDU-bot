from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def initiate_driver():
    options = Options()
    options.headless = True
    page_to_scrape = webdriver.Chrome(options=options)
    return page_to_scrape
