from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup  

def getDriverOptions():
    print("Initializing Browser Driver.")
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return options

def getBrowserInstance():
    return webdriver.Firefox(options=getDriverOptions(), executable_path = 'geckodriver')

def getWebpage(browser, url, expectedElement = None):
    browser.get(url)
    if expectedElement != None:
        try:
            timeout = 2
            expectedElement = EC.presence_of_element_located((By.CLASS_NAME, expectedElement))
            WebDriverWait(browser, timeout).until(expectedElement)
        except TimeoutException:
            print("Did not get page.")
    html = browser.page_source
    return BeautifulSoup(html, 'lxml')