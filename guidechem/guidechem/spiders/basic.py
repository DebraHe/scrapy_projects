# -*- coding: utf-8 -*-
import codecs
import sys
import urlparse

import scrapy
from scrapy_redis.spiders import RedisSpider

from guidechem.items import BasicItem
from tool.tool import drop_bom, drop_mark, unicode_to_str

reload(sys)
sys.setdefaultencoding('utf8')

_META_VERSION = 'v1.0'


class BasicSpider(RedisSpider):
    name = "basic"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'guidechem.pipelines.BasicPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'guidechem.middlewares.AbuyunProxyMiddleware': 90,
        },
    }

    def start_requests(self):
        over = {}
        with codecs.open('doc/done.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                over[line.strip()] = 1
        with codecs.open('doc/notyet.txt', 'r', encoding='utf-8') as f:
            for kw in f.readlines():
                if kw.strip() in over:
                    continue

                # drop BOM header
                url_str = drop_bom(kw)

                yield scrapy.http.Request(
                    url='http://china.guidechem.com/product/dict-search.jsp?keys={}'.format(url_str),
                    meta={'kw': kw.strip()},
                    callback=self.parse_list
                )

    def parse_list(self, response):
        lists = response.css('div.product_list_leftt dl dd')
        names = lists.css('div.duct_lis_left div.duct_lis_top em::text').extract()
        kw = response.meta.get('kw')

        self.logger.info(kw)
        get_fit_kw = 0
        for i, name in enumerate(names):
            if drop_bom(name) == drop_bom(kw):
                detail_url = lists[i].css('div.duct_lis_left div.duct_lis_top a::attr(href)').extract_first()
                pic = lists[i].css('table.duct_lis_right img::attr(src)').extract_first()
                get_fit_kw = 1
                yield scrapy.http.Request(
                    url=urlparse.urljoin(response.url, detail_url),
                    meta={'kw': kw.strip(), 'name': name, 'pic': pic},
                    callback=self.parse_detail
                )

        if not get_fit_kw:
            detail_url = lists[0].css('div.duct_lis_left div.duct_lis_top a::attr(href)').extract_first()
            pic = lists[0].css('table.duct_lis_right img::attr(src)').extract_first()
            yield scrapy.http.Request(
                url=urlparse.urljoin(response.url, detail_url),
                meta={'kw': kw.strip(), 'name': names[0], 'pic': pic},
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        info = {}
        item = BasicItem()
        item['kw'] = response.meta.get('kw')
        item['url'] = response.url
        item['image_url'] = response.meta.get('pic')
        item['name'] = response.meta.get('name')

        # chanpinmiaoshu
        chanpinmiaoshu = '\n'.join(response.xpath('//div[@id="f_1"]/../div[@class="pr_stv_center"]/text()').extract())
        if chanpinmiaoshu:
            info['产品描述'] = chanpinmiaoshu
        else:
            chanpinmiaoshu = '\n'.join(
                response.xpath('//div[@id="f_1"]/../div[@class="pr_stv_center"]/p/text()').extract())
            if chanpinmiaoshu:
                info['产品描述'] = chanpinmiaoshu

        # msds
        msds_name = response.css('div#msds div.pr_stv_cen_tert4 div span::text').extract()
        msds_expre = response.css('div#msds div.pr_stv_cen_tert4 div').re(r'</span>[\s]{0,2}(.*?)<br>')
        if len(msds_name) == len(msds_expre):
            for name, expre in zip(msds_name, msds_expre):
                info[name.rstrip(u'：')] = expre

        # jiben
        jibens = response.css('div#jiben div.pr_stv_centert ul li')
        for jiben in jibens:
            jiben_name = jiben.css('span::text').extract_first().rstrip(u'：')
            jiben_expre = jiben.css('em').xpath('string(.)').extract_first()
            if not jiben_expre:
                jiben_expre = jiben.css('em a::text').extract_first()
            info[jiben_name] = jiben_expre

        # wuhua
        wuhuas = response.css('div#wuhua div.pr_stv_centert ul li')
        for wuhua in wuhuas:
            wuhua_name = wuhua.css('span::text').extract_first().rstrip(u'：')
            wuhua_expre = wuhua.css('em::text').extract_first()
            if not wuhua_expre:
                wuhua_expre = wuhua.css('em a::text').extract_first()
            info[wuhua_name] = wuhua_expre

        # anquan
        anquans = response.css('div#anquan div.pr_stv_centert ul li')
        for anquan in anquans:
            anquan_name = anquan.css('span::text').extract_first().rstrip(u'：')
            anquan_expre = anquan.css('em::text').extract_first()
            if not anquan_expre:
                anquan_expre = anquan.css('em a::text').extract_first()
            info[anquan_name] = anquan_expre

        # yongtu
        yongtus = response.css('div#yongtu div.pr_stv_cen_tert em').extract()
        if len(yongtus) == 1:
            info['用途'] = drop_mark(yongtus[0])

        if len(yongtus) == 2:
            info['生产方法'] = drop_mark(yongtus[0])
            info['用途'] = drop_mark(yongtus[1])

        # haiguan
        haiguans = response.css('div#haiguan div.pr_stv_cen_tert2 ul li')
        for haiguan in haiguans:
            haiguan_name = haiguan.css('span::text').extract_first().rstrip(u'：')
            haiguan_expre = haiguan.css('em::text').extract_first()
            if not haiguan_expre:
                haiguan_expre = haiguan.css('em a::text').extract_first()
            info[haiguan_name] = haiguan_expre

        # toxi
        toxis = response.css('div#toxi div.pr_stv_centert ul li')
        for toxi in toxis:
            toxi_name = toxi.css('span::text').extract_first().rstrip(u'：')
            toxi_expre = toxi.css('em::text').extract_first()
            if not toxi_expre:
                toxi_expre = toxi.css('em a::text').extract_first()
            info[toxi_name] = toxi_expre

        # chemdata
        chemdata = response.css('div#chemdata div.pr_stv_cen_tert4 em').re(r'<em>(.*?)</em>')
        if chemdata:
            info['计算化学数据'] = drop_mark(chemdata[0])

        # 上下游产品
        shangxiayous = response.css('div#shangxiayou div.pr_stv_cen_tert7 div.tv_cen_te2')
        if len(shangxiayous) >= 1:
            shangyous = shangxiayous[0].css('dl dd')
            dict_shangyou = {}
            for shangyou in shangyous:
                image_url = urlparse.urljoin(response.url, shangyou.css('img::attr(src)').extract_first())
                name = shangyou.css('em a::text').extract_first()
                dict_shangyou[name] = image_url
            for key in dict_shangyou:
                dict_shangyou[key] = unicode_to_str(dict_shangyou[key])
            info['上游产品'] = dict_shangyou
        if len(shangxiayous) == 2:
            xiayous = shangxiayous[1].css('dl dd')
            dict_xiayou = {}
            for xiayou in xiayous:
                image_url = urlparse.urljoin(response.url, xiayou.css('img::attr(src)').extract_first())
                name = xiayou.css('em a::text').extract_first()
                dict_xiayou[name] = image_url
            for key in dict_xiayou:
                dict_xiayou[key] = unicode_to_str(dict_xiayou[key])
            info['下游产品'] = dict_xiayou

        for key in info:
            info[key] = unicode_to_str(info[key])
        item['info'] = info
        return item

