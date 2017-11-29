# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from tianyancha.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
import time
import datetime


class TycLoginMiddleware(object):
    def __init__(self, settings):
        self.download_delay = settings.get('DOWNLOAD_DELAY')
        self.url = 'https://www.tianyancha.com/login'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if not request.meta.get('login'):
            return
        if spider.driver:
            spider.driver.quit()
            spider.driver = None
        spider.flag = False
        # dcap = dict(DesiredCapabilities.CHROME)

        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.disk-cache"] = True
        cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        path = '/Users/debrahe/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'
        driver = webdriver.PhantomJS(path, desired_capabilities=cap)
        driver.get('https://www.tianyancha.com/login')
        time.sleep(10)
        driver.save_screenshot('screen.jpg')
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.loginmodule')),
            'login fail'
        )
        driver.save_screenshot('screen.jpg')
        username_str = 'xxx'
        password_str = 'xxx'
        username = driver.find_element_by_css_selector('div.mobile_box input.contactphone')
        username.clear()
        username.send_keys(username_str)
        password = driver.find_element_by_css_selector('div.mobile_box input.contactword')
        password.clear()
        password.send_keys(password_str)
        driver.find_element_by_css_selector('div.mobile_box div.login_btn').click()

        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input#home-main-search')),
            "login fail"
        )

        driver.save_screenshot('screen.jpg')
        body = driver.page_source
        spider.flag = True
        spider.driver = driver
        driver.save_screenshot(str("登录界面.jpg"))
        time.sleep(self.download_delay)
        print "login"
        return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)

    def process_exception(self, request, exception, spider):
        print '-------------------------'
        print type(exception)
        print '-------------------------'
        if spider.driver:
            spider.driver.save_screenshot(str("登录出错.jpg"))
            spider.driver.quit()
        return HtmlResponse(request.url, body="", encoding='utf-8', request=request)


class TycListMiddleware(object):
    def __init__(self, settings):
        self.download_delay = settings.get('DOWNLOAD_DELAY')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        while not spider.driver:
            print 'login............'
            time.sleep(1)
        driver = spider.driver
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        driver.get(request.url)
        WebDriverWait(driver,1, 0.3).until(
            ec.presence_of_element_located((By.XPATH, '//div[@class="b-c-white search_result_container"] | //img[@alt="无结果"]')),
            'code'
        )
        body = driver.page_source
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        print datetime.datetime.now()
        time.sleep(self.download_delay)
        return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)

    def process_exception(self, request, exception, spider):
        print type(exception)
        return HtmlResponse(request.url, body="", encoding='utf-8', request=request)


class TycDetailMiddleware(object):
    def __init__(self, settings):
        self.download_delay = settings.get('DOWNLOAD_DELAY')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        while not spider.driver:
            print 'waiting for login......'
            time.sleep(1)
        driver = spider.driver
        spider.flag = False
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        driver.get(request.url)
        WebDriverWait(driver,1,0.2).until(
            ec.presence_of_element_located((By.XPATH, '//div[@class="container company_container"]'))
        )
        body = driver.page_source
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        print str(datetime.datetime.now())[11:]
        time.sleep(self.download_delay)
        spider.flag = True
        return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)

    def process_exception(self, request, exception, spider):
        print '>>', type(exception)
        if isinstance(exception, TimeoutException):
            spider.flag = False
            while 1:
                pass
        return HtmlResponse(request.url, body="", encoding='utf-8', request=request)
