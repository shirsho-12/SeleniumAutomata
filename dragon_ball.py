import os
import wget
import urllib
import bs4
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by

browser = webdriver.Chrome()
failed_arr = [2, 3, 4, 6, 8, 10]
pass_but_fail = []


def xpath_clicker(link, time=3):
    try:
        WebDriverWait(browser, time).until(EC.presence_of_element_located((by.By.XPATH, link)))
        button = browser.find_element_by_xpath(link)
        browser.execute_script('arguments[0].click();', button)
        return 1
    except TimeoutException:
        return 0
        # break


def text_clicker(text, time=5):
    try:
        WebDriverWait(browser, time).until(EC.presence_of_element_located((by.By.LINK_TEXT, text)))
        button = browser.find_element_by_link_text(text)
        browser.execute_script('arguments[0].click();', button)
        # browser.click(button)
        return 1
    except TimeoutException:
        return 0


def extract_link(prompt=None, condition=None):
    soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
    req_link = None
    for link in soup.findAll('a', attrs={'href': re.compile("^https://{0}".format(prompt))}):
        if condition:
            if condition in link.text:
                print(link.get('href'))
                req_link = link.get('href')
        else:
            print(link.get('href'))
            req_link = link.get('href')
    return req_link


def download(link, ep_num, path='F:/', anime_name = 'Dragon Ball'):
    path += anime_name + '/'
    if not os.path.exists(path):
        os.mkdir(path)

    save_name = '{0} {1}.mp4'.format(anime_name, ep_num)
    save_name = path + save_name
    if os.path.exists(save_name):
        print("File exists")
        return 0
    trial = 0
    while True:
        try:
            urllib.request.urlretrieve(link + '.mp4', save_name)
            trial += 1
            print("Download of EP {0} COMPLETED".format(ep_num))
            return 0
        except Exception as e:
            trial +=1
            print(e)
        if trial == 5:
            print("DOWNLOAD FAILED EP", ep_num)
            failed_arr.append(ep_num)
            pass_but_fail.append(ep_num)
            return 0


    # wget.download(link)


def run(num_episodes, main_link = "https://www17.gogoanime.io/dragon-ball-dub-episode-"):

    for ep_num in range(11, num_episodes + 1):
        init_link = main_link +  str(ep_num)
        browser.get(init_link)

        xpath = '//*[@id="wrapper_bg"]/section/section[1]/div[1]/div[2]/div[1]/a[2]'
        WebDriverWait(browser, 6).until(EC.presence_of_element_located((by.By.XPATH, xpath)))
        browser.execute_script("window.stop()")


        link = extract_link('vidstreaming.io')
        browser.get(link)
        link_2 = extract_link('gcloud')
        browser.get(link_2)
        x_path_link = '//*[@id="download"]'
        click = xpath_clicker(x_path_link)
        print(click)
        if not click:
            failed_arr.append(ep_num)
            print("DOWNLOAD FAILED EP ", ep_num)
            continue
        time.sleep(10)
        download_link = extract_link('fvs', '720p')
        infinite_loop_counter = 0
        while download_link is None:
            time.sleep(2)
            infinite_loop_counter += 1
            click = xpath_clicker(x_path_link)
            download_link = extract_link('fvs', '720p')
            if infinite_loop_counter == 10:
                print("DOWNLOAD FAILED EP ", ep_num)
                failed_arr.append(ep_num)
                pass_but_fail.append(ep_num)
        download(download_link, ep_num)

    return failed_arr


def test():
    num_episodes = 153
    print(run(num_episodes))
    print("Episodes not available:", end=' ')
    for ep in failed_arr:
        print(ep, end=' ')
    print("Download failed episodes:", end=' ')
    for ep in pass_but_fail:
        print(ep, end=' ')


if __name__ == "__main__":
    test()
