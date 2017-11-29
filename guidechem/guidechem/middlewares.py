# -*- coding: utf-8 -*-
import base64
import logging


class AbuyunProxyMiddleware(object):

    def __init__(self, settings):
        self.logger = logging.getLogger('scrapy.proxies')
        self.proxyServer = "http://proxy.abuyun.com:9020"
        proxyUser = "XXX"
        proxyPass = "XXX"
        self.proxyAuth = "Basic " + \
            base64.b64encode(proxyUser + ":" + proxyPass)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        if spider.host in request.url:
            self.logger.debug("Proxy exception %(request)s",
                              {'request': request},
                              extra={'spider': spider})
        retryreq = request.copy()
        retryreq.dont_filter = True
        return retryreq