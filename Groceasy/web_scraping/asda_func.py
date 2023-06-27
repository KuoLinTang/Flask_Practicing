from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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

    element.clear()
    element.send_keys(item_name)
    time.sleep(1)
    element.send_keys(Keys.ENTER)


def fetch_top_items(driver, xpath: str, n: int):

    try:
        element_list = WebDriverWait(driver=driver, timeout=timeout).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(e)
    else:
        print(element_list[:n])
