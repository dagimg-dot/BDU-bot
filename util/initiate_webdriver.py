from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def initiate_driver():
    options = Options()
    options.headless = True
    page_to_scrape = webdriver.Chrome(executable_path='./chromedriver.exe', port=8000, options=options)
    return page_to_scrape
