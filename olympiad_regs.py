import csv
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


browser = webdriver.Chrome()

passwords = ["rifat03cgs", 'victor04cgs', 'hina05cgs', 'farjana06cgs', 'naznin07cgs', 'suman08cgs']
for i in range(3, 9):
    file_name = ("data/Class " + str(i) + ".csv")
    print("Class " + str(i))
    with open(file_name) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        password_str = passwords[i-3]

        for row in reader:
            browser.get("http://online.matholympiad.org.bd/login")
            WebDriverWait(browser, 1)
            username = browser.find_element_by_id("username")
            username.send_keys(row[2])
            password = browser.find_element_by_id("password")
            password.send_keys(password_str)
            WebDriverWait(browser, 1)
            button_1 = browser.find_element_by_css_selector(".footer")
            button_1.click()
            try:
                WebDriverWait(browser, 1)
                button_2 = browser.find_element_by_xpath('//*[@id="navigation"]/ul/li[3]/a')
                button_2.click()
            except NoSuchElementException:
                print(row)
browser.close()
