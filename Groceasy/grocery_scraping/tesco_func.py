from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

timeout = 10


def search_item(driver, xpath: str, item_name: str):

    element = WebDriverWait(driver=driver, timeout=timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )

    element.send_keys(item_name)
    element.send_keys(Keys.ENTER)


def fetch_top_items(driver: webdriver, n: int):

    # define class names for different info
    name_volume_class = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/ul/li[*]/div/div/div/div[1]'
    price_class = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/ul/li[4]/div/div/div/div/div[1]/div[3]/div/div/form/div/div/div[1]/p[1]'
    price_per_unit_class = 'styled__StyledFootnote-sc-119w3hf-7 icrlVF styled__Subtext-sc-8qlq5b-2 bNJmdc beans-price__subtext'
    img_class = 'styled__Image-sjvkdn-0 bJErKA product-image beans-responsive-image__image'
    #
    class_name_list = [name_volume_class, price_class,
                       price_per_unit_class, img_class]

    def fetch_item_info(driver: webdriver, class_name: str, n: int):

        try:
            elements = WebDriverWait(driver=driver, timeout=timeout).until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, class_name))
            )
            top_n_elements = elements[:min(len(elements), n)]
            if class_name.endswith('image'):
                contents = [i.get_attribute('src') for i in top_n_elements]
            else:
                # get text from the element
                contents = [i.text for i in top_n_elements]
        except Exception as e:
            print(e)
        else:
            return contents

    # result
    results = list(zip(*[fetch_item_info(driver=driver, class_name=i, n=n)
                         for i in class_name_list]))

    return results


def tesco(item: str = 'milk'):

    chrome_options = webdriver.ChromeOptions()
    # not opening a browser while avoiding being detected
    # chrome_options.add_argument('--headless=new')
    # chrome_options.add_argument(
    #     '--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://www.tesco.com/')

    search_bar_xpath = '//*[@id="beans-masthead-desktop-search-input"]'
    top_n = 5

    search_item(browser, search_bar_xpath, item)
    # results = fetch_top_items(browser, n=top_n)

    elements = WebDriverWait(driver=browser, timeout=timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/ul/li[3]/div/div/div/div'))
    )

    print(elements.get_attribute('id'))
    time.sleep(600)
    browser.quit()

    # return results


tesco('milk')
