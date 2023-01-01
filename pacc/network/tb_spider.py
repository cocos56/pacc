"""淘宝账号注册爬虫模块"""
from selenium import webdriver


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
        """淘宝账号注册爬虫程序入口方法"""
        cls.driver.get('https://ipp.alibabagroup.com/register.htm')
        cls.driver.maximize_window()
        # cls.open_url_in_new_window('https://ipp.alibabagroup.com/login.htm')


if __name__ == '__main__':
    Spider.main()
