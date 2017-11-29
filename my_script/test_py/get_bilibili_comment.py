# -*- coding: utf-8 -*-
from lxml import etree
from selenium import webdriver


class BibiliCommentSpider:

    driver = webdriver.PhantomJS()  # 使用webdriver.PhantomJS

    def get_url_content(self, url):
        self.init_phantom_driver(url)

    def init_phantom_driver(self, url):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'
        headers = {
            'User-Agent': user_agent,
        }

        for key, value in headers.iteritems():
            cap['phantomjs.page.customHeaders.{}'.format(key)] = value
            cap['phantomjs.page.customHeaders.User-Agent'] = user_agent
            self.driver = webdriver.PhantomJS(desired_capabilities=cap)

        self.driver.get(url)
        doctree = self.get_dom_tree()
        print doctree

    def get_dom_tree(self):
        # 执行js得到整个dom
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        doctree = etree.HTML(html)
        print type(doctree)
        return doctree


url = "https://www.bilibili.com/video/av14669747/"
spider = BibiliCommentSpider()
spider.get_url_content(url)
