from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

timeout = 10


def search_item(driver, xpath: str, item_name: str):

    element = WebDriverWait(driver=driver, timeout=timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )

    element.send_keys(item_name)
    element.send_keys(Keys.ENTER)


def fetch_top_items(driver: webdriver, n: int):

    # define class names for different info
    name_volume_xpath = './/a[@class="styled__Anchor-sc-1xbujuz-0 csVOnh beans-link__anchor"]'
    price_xpath = './/p[@class="styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text"]'
    price_per_unit_xpath = './/p[@class="styled__StyledFootnote-sc-119w3hf-7 icrlVF styled__Subtext-sc-8qlq5b-2 bNJmdc beans-price__subtext"]'
    #
    xpath_list = [name_volume_xpath, price_xpath, price_per_unit_xpath]

    def fetch_item_info(driver: webdriver, xpath: str, n: int):

        def split_by_number(string: str):

            match = re.findall(r'\d+', string)
            if len(match) > 0:  # matched
                number = match[0]  # get matched number
                index = string.index(number)  # find the index of the number
                return (string[:index].strip(), string[index:].strip())
            else:  # unmatched
                return (string, None)

        # start to process
        try:
            elements = WebDriverWait(driver=driver, timeout=timeout).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, xpath))
            )
            top_n_elements = elements[:min(len(elements), n)]

            if xpath.startswith('.//a'):  # split item name and volume
                contents = [split_by_number(i.text) for i in top_n_elements]
            else:
                # get text from the element
                contents = [i.text for i in top_n_elements]
        except Exception as e:
            print(e)
        else:
            return contents

    # result
    results = list(zip(*[fetch_item_info(driver=driver, xpath=i, n=n)
                         for i in xpath_list]))

    return results


def tesco(item: str = 'milk', n: int = 5):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    # not opening a browser while avoiding being detected
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument(
        '--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://www.tesco.com/')

    search_bar_xpath = '//*[@id="beans-masthead-desktop-search-input"]'

    search_item(browser, search_bar_xpath, item)
    results = fetch_top_items(browser, n=n)
    results = [(i[0][0], i[0][1], i[1], i[2]) for i in results]

    browser.quit()

    return results
