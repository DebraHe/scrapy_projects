# -*- coding: utf-8 -*-

# Scrapy settings for chemall51 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chemall51'

SPIDER_MODULES = ['chemall51.spiders']
NEWSPIDER_MODULE = 'chemall51.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Override the default request headers:
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

AWS_ACCESS_KEY_ID = "AKIAPTROC32OLSHTXD4A"
AWS_SECRET_ACCESS_KEY = "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"
MEDIA_ALLOW_REDIRECTS = True
CLOUD_MODE = 0
if CLOUD_MODE:
    SCHEDULER = "scrapy_redis.scheduler.Scheduler"
    DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
    SCHEDULER_PERSIST = False
    REDIS_URL = 'redis://10.9.161.8:6379'
