# -*- coding: utf-8 -*-

# Scrapy settings for qingting project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qingting'

SPIDER_MODULES = ['qingting.spiders']
NEWSPIDER_MODULE = 'qingting.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qingting (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 128

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
#    'Host': '',
#    'Origin':'',
#    'Referer': '',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qingting.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
    # 'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
    # 'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'qingting.middlewares.UserAgentMiddleware': 400,
    # 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
    # 'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
    # 'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
    # 'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
    # 'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
    # 'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
    # 'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
    # 'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
    # 'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    # 'qingting.pipelines.QingtingPipeline': 300,
#    # 'qingting.pipelines.MongoDBPipleline': 301
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

CLOUD_MODE = 0
if CLOUD_MODE:
    SCHEDULER = "scrapy_redis.scheduler.Scheduler"
    DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
    SCHEDULER_PERSIST = False
    REDIS_URL = 'redis://:76xD=3{Qi=Exvcw4@10.9.107.220:6379'

# Proxy
DOWNLOAD_TIMEOUT = 60
PROXY_LIMIT = 300
MIN_PROXY_NUM = 100
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
