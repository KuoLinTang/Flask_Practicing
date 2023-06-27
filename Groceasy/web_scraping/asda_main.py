from selenium import webdriver
from asda_func import accept_privacy_term, search_item, fetch_top_items
import time

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://groceries.asda.com/')

# browser.find_elements(by=, value=)
time.sleep(1)
accept_privacy_term(browser, '//*[@id="onetrust-accept-btn-handler"]')

time.sleep(2)
search_item(browser, '//*[@id="search"]', 'Milk')

time.sleep(2)
fetch_top_items(
    browser, '//*[@id="main-content"]/main/div[2]/div/div[4]/div/div[2]/ul/', n=10)

time.sleep(600)
browser.quit()
