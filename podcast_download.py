import os
import wget
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by

from basic_utils import get_folder_name, make_soup, name_func
from scrapy.selector import Selector

# Global variable browser
browser = webdriver.Chrome()

"""
Deprecated for direct usage
def browser_back_to_main():
    main_page = 'https://podcasts.google.com/?feed=aHR0cHM6Ly9sZXhmcmlkbWFuLmNvbS9jYXRlZ29yeS9haS9mZWVkLw'
    browser.get(main_page)
"""


def link_finder(box=False, num_val = None):
    # print(url)
    soup = make_soup(browser.page_source)
    # print(soup.soupify)
    if box:
        link_arr = soup.find('div', attrs={'jscontroller': "ORTa9"})
        # print(link_arr['data-link'])
        if link_arr:
            return link_arr['data-link']
    else:
        if not num_val:
            for i in range(6):
                try:
                    if i == 0:
                        path = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/div/div[2]/div/div[3]/div[1]'
                    else:
                        path = '//*[@id="yDmH0d"]/c-wiz[' + str(i) + ']/div/div[2]/div/c-wiz/' \
                                                                     'div/div[2]/div/div[3]/div[1]'

                    WebDriverWait(browser, 3).until(EC.presence_of_element_located((by.By.XPATH, path)))
                    WebDriverWait(browser, 3).until(EC.element_to_be_clickable((by.By.XPATH, path)))
                    return path, i

                except ElementNotInteractableException or TimeoutException:
                    continue


def search(obj):
    google_search_bar_path = '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((by.By.XPATH, google_search_bar_path)))
    search_box = browser.find_element_by_xpath(google_search_bar_path)
    search_box.send_keys(obj + " google podcasts")
    search_button = browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
    search_button.click()

    box_link = link_finder(box=True)
    browser.get(box_link)

    main_page_path = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/div/div[2]/div/a'
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((by.By.XPATH, main_page_path)))
    main_page_button = browser.find_element_by_xpath(main_page_path)
    main_page_button.click()
    return browser.current_url


def download(data_array):
    """Downloads audio files into specified folder"""
    for link, name in data_array:
        folder_name = name_func(get_folder_name(data_array[0][1]))
        new_path = os.path.abspath(os.getcwd()) + folder_name
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        file_name = name_func(name.replace(' -' + folder_name[1:], '.mp3'))
        file_path = new_path + file_name
        print(folder_name, '\n', file_name)
        wget.download(link, file_path)


def data_extract():
    # Get download links and file names for saving
    play_path, num = link_finder()
    try:
        # CHANGE TO BEAUTIFUL SOUP METHOD BY SEARCHING "PLAY EPISODE" STRING INSTEAD OF XPATH - STRING DOES NOT WORK
        # DIFFERENT c-wiz values for different pages
        # play_path = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div/div[2]/div/div[3]/div[1]'
        play_path = link_finder(num_val=num)
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((by.By.XPATH, play_path)))
        play_button = browser.find_element_by_xpath(play_path)
        play_button.click()

    except TimeoutException:
        print("Error")
        raise Exception
        pass

    page_soup = make_soup(browser.page_source)

    audio_data = page_soup.find('audio')
    link = audio_data['src']
    title = audio_data['title']
    # print(link, '\n', title)
    return [link, title]


def podcast_click(main_page, ep_num):
    data_arr = []        # data_arr : [[link, title]]
    i = 1
    while True:
        path = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/div/div[2]/div/c-wiz/div/div[2]/a[' + str(i) + ']'
        i += 1
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located((by.By.XPATH, path)))
            button = browser.find_element_by_xpath(path)
            browser.execute_script('arguments[0].click();', button)
            data_arr.append(data_extract())
            browser.get(main_page)
            # browser_back_to_main()
            print("Found ", i - 1)
            if i > ep_num:
                browser.close()
                download(data_arr)
                # print(data_arr)
                break
        except TimeoutException:
            print("Podcast completed")
            break


def run(search_term, num):

    browser.get("http://www.google.com")
    main_page = search(search_term)
# soup = make_soup(browser.page_source)
# browser_back_to_main()

    podcast_click(main_page, num)


def test():
    run(search_term='lex fridman podcast', num=1)


# test()