# -*- coding: utf-8 -*-

import logging
import random
import time

from tool.tool import get_proxy


class RandomProxy(object):
    def __init__(self, settings):
        self.logger = logging.getLogger('scrapy.proxies')
        self.proxies = {}
        self.proxy_limit = settings.get('PROXY_LIMIT')
        self.min_proxy_num = settings.get('MIN_PROXY_NUM')
        for _ in get_proxy(self.proxy_limit):
            self.proxies[_] = ''

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        # if 'proxy' in request.meta:
        #     return

        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')
        # add more proxies
        if len(self.proxies) < self.min_proxy_num:
            time.sleep(1)
            for _ in get_proxy(self.proxy_limit):
                self.proxies[_] = ''
            self.logger.info('now have {} proxies'.format(len(self.proxies)))

        proxy_address = random.choice(list(self.proxies.keys()))
        request.meta['proxy'] = proxy_address
        self.logger.debug('Using proxy <%s>, %d proxies left' % (
            proxy_address, len(self.proxies)))

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return

        proxy = request.meta['proxy']
        try:
            del self.proxies[proxy]
        except KeyError:
            pass

        self.logger.info('Removing failed proxy {}, {} proxies left'.format(
            proxy, len(self.proxies)))
