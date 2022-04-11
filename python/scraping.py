from time import sleep
from datetime import datetime
import re
import random
import pandas as pd
from functools import reduce
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


def rnd_sleep():
    """
    Generates random sleep times between 1 and 3 seconds
    :return: sleep class
    """
    return sleep(randint(1, 3))


def mouse_action(target, browser):
    """
    Moves mouse to element to trigger hover action.
    :param target: xpath to be interacted with.
    :param browser: selenium webdriver.
    :return: void
    """
    # Create the object for Action Chains
    actions = ActionChains(browser)
    actions.move_to_element(target)

    actions.move_to_element(target)

    # perform the operation on the element
    actions.perform()
    rnd_sleep()
    target.click()
    rnd_sleep()


def get_usr_ag():
    """
    Aux function that generates random user-agent for the http request header.
    :return: String.
    """
    usr_ag_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
                   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
                   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]

    return random.choice(usr_ag_list)


def create_browser():
    """
    Creates customized Chrome Driver.
    :return: selenium webdriver.
    """
    option = webdriver.ChromeOptions()

    # Creating window size. Code does only support this media query.
    option.add_argument("window-size=1280,800")

    # Random User-agent
    option.add_argument("user-agent=" + get_usr_ag())

    # Removes navigator.webdriver flag

    # For older ChromeDriver under version 79.0.3945.16
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    # For ChromeDriver version 79.0.3945.16 or over
    option.add_argument('--disable-blink-features=AutomationControlled')

    # Open Browser
    """IMPORTANT WARNING: BEFORE RUNNING CODE, CHANGE CHROMEDRIVER PATH"""
    path = 'C:\\Users\\alexo\\.wdm\\drivers\\chromedriver\\win32\\100.0.4896.60\\'
    browser = webdriver.Chrome(executable_path=path + 'chromedriver.exe',
                               options=option)

    return browser


def load_more(browser):
    """
    Clicks on Load More button several times.
    :param browser: selenium webdriver.
    :return: void.
    """
    xpath = '//tr['
    row_number = 150
    for i in range(1, 4):
        scroll_to = browser.find_element(By.XPATH, xpath + str(i * row_number) + ']')
        browser.execute_script("arguments[0].scrollIntoView();", scroll_to)
        load_more = browser.find_element(By.XPATH, '//span[@class="tv-load-more__btn"]')
        mouse_action(load_more, browser)
        rnd_sleep()
        sleep(1)


def crawl_table(browser_page):
    """
    Extracts and parses table content.
    :param browser_page: selenium webdriver page source.
    :return: pandas dataframe.
    """
    begin = datetime.now().strftime("[%H:%M:%S]")
    print("\n{} Extracting Table".format(begin))

    soup = BeautifulSoup(browser_page, 'html')
    head = soup.findAll('thead')[1]
    table = soup.findAll('tbody')[1]

    columns = []
    for row in head.find('tr'):
        for element in row.find('div', {'class': 'js-head-title tv-screener-table__head-left--title-three-lines'}):
            columns.append(element)

    df = pd.DataFrame([], columns=columns)
    count = 0
    for row in table.findAll('tr'):
        row_list = []
        count += 1
        for element in row.findAll('td'):
            text = element.get_text()
            row_list.append(re.sub('[\t\n]*', '', text))

        try:
            df.loc[len(df)] = row_list
        except ValueError:
            pass

    end = datetime.now().strftime("[%H:%M:%S]")
    print(df.head())
    print("\n{} Extracted successfully!".format(end))
    return df


def GetContent():
    browser = create_browser()

    browser.get("https://www.tradingview.com/")

    """
    Scroll down needed to make Cookies settings pop up.
    """
    browser.execute_script("window.scrollTo(0, 600)")
    sleep(1)
    browser.execute_script("window.scrollTo(0, 800)")
    sleep(1)
    browser.execute_script("window.scrollTo(0, 1200)")

    # Cookies
    target = browser.find_element(By.XPATH,
                                  '//button[@class="managePreferences-W4Y0hWcd button-YKkCvwjV size-xsmall-YKkCvwjV '
                                  'color-brand-YKkCvwjV variant-secondary-YKkCvwjV"]')

    mouse_action(target, browser)

    target = browser.find_element(By.XPATH,
                                  '//button[@class="savePreferences-vDbnNLqD button-YKkCvwjV size-medium-YKkCvwjV '
                                  'color-brand-YKkCvwjV variant-secondary-YKkCvwjV"]')

    mouse_action(target, browser)

    """
    Navigating Menu
    """
    # Menu Button
    target = browser.find_element(By.XPATH,
                                  '//button[@class="tv-header__hamburger-menu js-header-main-menu-mobile-button"]')

    mouse_action(target, browser)

    # Market
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="menuBox-8MKeZifP '
                                                                           'menuBox-kPwlL5Tr"]//div[@class="item-4TFSfyGO'
                                                                           ' item-ykcJIrqq item-KP3Lnocv '
                                                                           'withIcon-4TFSfyGO withIcon-ykcJIrqq"][''1]'))).click()

    rnd_sleep()

    # Crypto
    target = browser.find_element(By.XPATH,
                                  '//div[@class="content-kPwlL5Tr"]//div[@class="item-4TFSfyGO item-ykcJIrqq '
                                  'item-KP3Lnocv"][5]')
    mouse_action(target, browser)

    # Prices
    target = browser.find_element(By.XPATH,
                                  '//div[@class="content-kPwlL5Tr"]//a[@class="item-4TFSfyGO item-ykcJIrqq"][1]')
    mouse_action(target, browser)

    """
    Navigating table and extracting content
    """

    # Table buttons
    browser.execute_script("window.scrollTo(0, 1200)")

    # Load more Content
    load_more(browser)

    # Overview
    overview = crawl_table(browser.page_source)
    browser.execute_script("window.scrollTo(0, 1200)")

    rnd_sleep()

    # Next Buttons
    df_list = []
    for target in browser.find_elements(By.XPATH,
                                        '//div[@class="itemsWrap-1EEezFCx"]//div[@class="itemContent-1EEezFCx"]'):
        mouse_action(target, browser)
        load_more(browser)
        df_list.append(crawl_table(browser.page_source))
        browser.execute_script("window.scrollTo(0, 1200)")

    browser.quit()

    """
    Generating and extracting dataset
    """
    # Merging Dataframes
    df_list.append(overview)
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Name'],
                                                    how='outer'), df_list)

    # Dataset to csv
    today = datetime.now().strftime("%d_%m_%Y")
    file = '../data/' + today + '_cryptos.csv'
    df_merged.to_csv(file, index=False)

    csv_time = datetime.now().strftime("[%H:%M:%S]")
    print("\n{} csv file created!".format(csv_time))
