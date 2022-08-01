"""爬虫模块"""
import time

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By

from pacc.mysql.retrieve import RetrieveSD


START_INDEX = 20


class Spider:
    """爬虫类"""
    driver = webdriver.Chrome()

    @classmethod
    def open_url_in_new_window(cls, url=''):
        """在新窗口中打开URL

        :param url: 待打开的URL
        """
        cls.driver.execute_script(f"window.open('{url}')")

    @classmethod
    def main(cls):
        """程序入口方法"""
        RetrieveSD.all_names = RetrieveSD.all_names[START_INDEX:]
        for index, username in enumerate(RetrieveSD.all_accounts[START_INDEX:]):
            cls.driver.get('http://47.100.242.194/')
            cls.driver.maximize_window()
            time.sleep(4)
            print(index + 1, username, end=' ')
            password = 'k187397'
            cls.driver.find_element(By.ID, "username").send_keys(username)
            cls.driver.find_element(By.ID, "password").send_keys(password)
            cls.driver.find_element(
                By.XPATH, '//*[@class="ant-btn ant-btn-primary ant-btn-lg submit___Q43EO"]/span'
            ).click()
            time.sleep(3)
            cls.open_url_in_new_window('http://47.100.242.194/record/trades/')
            cls.open_url_in_new_window('http://47.100.242.194/record/linked')
            cls.open_url_in_new_window('http://47.100.242.194/account/buyers')
            cls.open_url_in_new_window('http://47.100.242.194/account/wallet')
            cls.driver.switch_to.window(cls.driver.window_handles[1])
            time.sleep(12)
            cls.driver.find_element(By.XPATH, '//*[@class="ant-btn ant-btn-primary"]/span').click()
            cls.driver.find_element(By.ID, "amount").send_keys('9999')
            cls.driver.find_element(By.ID, "tradeWayNo").send_keys('18739776523@qq.com')
            value = cls.driver.find_element(By.ID, "amount").get_attribute("value")
            print(RetrieveSD.all_names[index], value)
            cls.driver.find_element(By.ID, "realName").send_keys('徐可可')
            if float(value) >= 20:
                cls.driver.find_element(By.ID, "password").send_keys(password)
                cls.driver.find_element(
                    By.XPATH, '//*[@class="ant-modal-footer"]//*[@class="ant-btn ant-btn-primary"]'
                ).click()
                pyperclip.copy(f'{RetrieveSD.all_names[index]}	{value}')
                time.sleep(3)
                cls.driver.refresh()
            input()
            cls.driver.quit()
            if not index == len(RetrieveSD.all_accounts) - 1:
                cls.driver = webdriver.Chrome()


if __name__ == '__main__':
    Spider.main()
