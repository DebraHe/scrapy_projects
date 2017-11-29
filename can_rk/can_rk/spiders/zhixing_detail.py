# -*- coding: utf-8 -*-

import scrapy
import random
import json

from can_rk.items import CanRkItem
from tool.tool import get_code

_META_VERSION = 'v1.0'

from scrapy_redis.spiders import RedisSpider


class ZhixingSpider(RedisSpider):
    name = 'zhixing_detail'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'can_rk.pipelines.CanRkPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
        'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
    ]

    def make_requests_from_url(self, url):
        captchaId, code = get_code()
        return scrapy.Request(
            'http://zhixing.court.gov.cn/search/newdetail?id={}&j_captcha={}&captchaId={}'.format(url, code,
                                                                                                  captchaId),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': random.choice(self.user_agents),
                'Connection': 'keep-alive',
                'Host': 'zhixing.court.gov.cn'
            },
            callback=self.parse_info,
            meta={'person_id': url}
        )

    def parse_info(self, response):
        person_id = response.meta.get('person_id')
        try:
            info = json.loads(response.text)
            if info:
                with open('doc/succeed_id.txt', 'a') as f:
                    f.write(person_id + '\n')
                item = CanRkItem()
                item['url'] = response.url
                item['id'] = info.get('id')
                item['caseCode'] = info.get('caseCode')
                item['caseState'] = info.get('caseState')
                item['execCourtName'] = info.get('execCourtName')
                item['execMoney'] = info.get('execMoney')
                item['partyCardNum'] = info.get('partyCardNum')
                item['pname'] = info.get('pname')
                item['caseCreateTime'] = info.get('caseCreateTime')
                yield item
            else:
                captchaId, code = get_code()
                yield scrapy.Request(
                    'http://zhixing.court.gov.cn/search/newdetail?id={}&j_captcha={}&captchaId={}'.format(person_id, code,
                                                                                                          captchaId),
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': random.choice(self.user_agents),
                        'Connection': 'keep-alive',
                        'Host': 'zhixing.court.gov.cn'
                    },
                    callback=self.parse_info,
                    meta={'person_id': person_id}
                )
        except:
            captchaId, code = get_code()
            yield scrapy.Request(
                'http://zhixing.court.gov.cn/search/newdetail?id={}&j_captcha={}&captchaId={}'.format(person_id, code,
                                                                                                      captchaId),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': random.choice(self.user_agents),
                    'Connection': 'keep-alive',
                    'Host': 'zhixing.court.gov.cn'
                },
                callback=self.parse_info,
                meta={'person_id': person_id}
            )
