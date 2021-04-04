import urllib.request
from urllib.request import urlretrieve
import requests

from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def make_soup(text):
    return BeautifulSoup(text, 'html.parser')


def search(obj):
    search_box = browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    search_box.send_keys(obj)
    search_button = browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
    search_button.click()


def download_podcast(page):
    browser.get(page)
    WebDriverWait(browser, 10000)
    page_soup = make_soup(browser.page_source)
    title = page_soup.find('div', attrs={'class': 'JCi0he'})
    print(title)


browser = webdriver.Chrome()
browser.get("http://www.google.com")
# search("Lex Fridman podcast")
# soup = make_soup(browser.page_source)

file = open('E:\Python Projects\Selenium Automation\search_data\google_search_page.html', 'r', encoding='utf8')
soup = make_soup(file.read())
links = soup.findAll('div', attrs={'data-link': re.compile('^https://')})
for link in links:
    print(link)
    download_podcast(link['data-link'])
