from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

timeout = 10


def accept_privacy_term(driver, xpath: str):

    element = WebDriverWait(driver=driver, timeout=timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

    element.click()


def search_item(driver, xpath: str, item_name: str):

    element = WebDriverWait(driver=driver, timeout=timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )

    element.send_keys(item_name)
    element.send_keys(Keys.ENTER)


def fetch_top_items(driver: webdriver, n: int):

    # define xpath patterns for different info
    name_volume_xpath = './/a[@class="pt__link"]'
    price_xpath = './/span[@class="pt__cost__retail-price"]'
    price_per_unit_xpath = './/span[@class="pt__cost__unit-price-per-measure"]'
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

        try:
            elements = WebDriverWait(driver=driver, timeout=timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )
            top_n_elements = elements[:min(len(elements), n)]

            if xpath.startswith('.//a'):
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


def sainsbury(item: str = 'milk', n: int = 5):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    # not opening a browser while avoiding being detected
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument(
        '--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://www.sainsburys.co.uk/')

    term_accept_xpath = '//*[@id="onetrust-accept-btn-handler"]'
    search_bar_xpath = '//*[@id="term"]'

    accept_privacy_term(browser, term_accept_xpath)
    search_item(browser, search_bar_xpath, item)
    results = fetch_top_items(browser, n=n)
    results = [(i[0][0], i[0][1], i[1], i[2]) for i in results]

    browser.quit()

    return results
