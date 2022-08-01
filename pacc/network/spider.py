"""爬虫模块"""
import time

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By

from pacc.mysql.retrieve import RetrieveSD

driver = webdriver.Chrome()


def open_url_in_new_window(url='', chrome_driver=driver):
    js = f"window.open('{url}')"
    chrome_driver.execute_script(js)


for index, username in enumerate(RetrieveSD.all_accounts[0:]):
    driver.get('http://47.100.242.194/')
    driver.maximize_window()
    time.sleep(1)
    print(index, username)
    password = 'k187397'
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(
        By.XPATH, '//*[@class="ant-btn ant-btn-primary ant-btn-lg submit___Q43EO"]/span').click()
    time.sleep(3)
    open_url_in_new_window('http://47.100.242.194/account/buyers')
    open_url_in_new_window('http://47.100.242.194/account/wallet')
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@class="ant-btn ant-btn-primary"]/span').click()
    driver.find_element(By.ID, "amount").send_keys('9999')
    driver.find_element(By.ID, "tradeWayNo").send_keys('18739776523@qq.com')
    value = driver.find_element(By.ID, "amount").get_attribute("value")
    print(value)
    pyperclip.copy(f'{RetrieveSD.all_names[index]}	{value}')
    driver.find_element(By.ID, "realName").send_keys('徐可可')
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(
        By.XPATH, '//*[@class="ant-modal-footer"]//*[@class="ant-btn ant-btn-primary"]').click()
    input()
    driver.quit()
    if not index == len(RetrieveSD.all_accounts)-1:
        driver = webdriver.Chrome()
