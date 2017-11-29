# -*- coding: utf-8 -*-

# Scrapy settings for weixin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weixin'

SPIDER_MODULES = ['weixin.spiders']
NEWSPIDER_MODULE = 'weixin.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weixin (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
# REDIRECT_ENABLED = False
'''
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'mp.weixin.qq.com',
    'If-Modified-Since': 'Wed, 3 May 2017 11:14:52 +0800',
    'Referer': 'http://weixin.sogou.com/weixin?p=01030402&query=%E8%B5%9B%E6%9F%8F%E8%93%9D&type=2&ie=utf8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36'
}
'''
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    # 'Host': 'www.xiami.com',
    # 'Referer': 'http://www.xiami.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
PHANTOMJS_DRIVER_PATH = '/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
CHROME_DRIVER_PATH = '/home/ubuntu/chromedriver'

CONCURRENT_REQUESTS = 1
