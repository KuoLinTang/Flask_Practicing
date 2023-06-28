from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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
    name_xpath = '//*[@id="main-content"]/main/div[2]/div/div[4]/div/div[2]/ul/li[*]/div/div/div[2]/div[1]/h3/a'
    volume_xpath = '//*[@id="main-content"]/main/div[2]/div/div[4]/div/div[2]/ul/li[*]/div/div/div[1]/div/div[2]/span'
    price_xpath = '//*[@id="main-content"]/main/div[2]/div/div[4]/div/div[2]/ul/li[*]/div/div/div[3]/div[1]/span/strong'
    price_per_unit_xpath = '//*[@id="main-content"]/main/div[2]/div/div[4]/div/div[2]/ul/li[*]/div/div/div[3]/div[1]/span/p/span'
    img_xpath = '//*[@id="main-content"]/main/div[2]/div/div[4]/div/div[2]/ul/li[*]/div/div/div[1]/button/div/picture/img'
    xpath_list = [name_xpath, volume_xpath,
                  price_xpath, price_per_unit_xpath, img_xpath]

    def fetch_item_info(driver: webdriver, xpath: str, n: int):

        try:
            elements = WebDriverWait(driver=driver, timeout=timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )
            top_n_elements = elements[:min(len(elements), n)]
            if xpath.endswith('img'):
                contents = [i.get_attribute('src') for i in top_n_elements]
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


# main process
def asda(item: str = 'milk'):

    chrome_options = webdriver.ChromeOptions()
    # not opening a browser while avoiding being detected
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument(
        '--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://groceries.asda.com/')

    term_accept_xpath = '//*[@id="onetrust-accept-btn-handler"]'
    search_bar_xpath = '//*[@id="search"]'
    top_n = 5

    accept_privacy_term(browser, term_accept_xpath)
    search_item(browser, search_bar_xpath, item)
    results = fetch_top_items(browser, n=top_n)
    browser.quit()

    return results
