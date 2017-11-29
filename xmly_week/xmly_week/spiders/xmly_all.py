# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.selector import Selector
from xmly_week.items import XmlyInfoItem
from xmly_week.items import XmlyDetailItem
import re
_META_VERSION = 'v1.0'


class XmlyChildSpider(scrapy.Spider):
    name = 'xmly_all'
    meta_version = _META_VERSION
    result_dir = './result'
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'ITEM_PIPELINES': {
            'xmly_week.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(url='http://www.ximalaya.com/dq/')

    def parse(self, response):
        categories = [
            {
                'key': 'renwen',
                'first_level': '人文',
                'second_level': ['经典名著', '诗词歌赋']
            },
            {
                'key': 'entertainment',
                'first_level': '娱乐',
                'second_level': ['段子笑话', '脱口秀']
            },
            {
                'key': 'english',
                'first_level': '英语',
                'second_level': ['名著', '少儿']
            },
            {
                'key': 'poem',
                'first_level': '诗歌',
                'second_level': ['古诗词', '诗词歌赋', '启蒙']
            }
        ]
        for category in categories:
            for second_level in category['second_level']:
                yield scrapy.Request(
                    url='http://www.ximalaya.com/dq/{}-{}/1/'.format(category['key'], second_level),
                    callback=self.parse_list,
                    meta={
                        'key': category['key'],
                        'first_level': category['first_level'],
                        'second_level': second_level
                    }
                )
        request_list = ['儿童', '戏曲', '相声评书']
        categories = []

        response_panel = response.css('div#discoverAlbum div.layout_left div.dis_sound_sort ul.sort_list')
        for big_item in response_panel.css('li'):
            categories_dict = {
                'id': '',
                'key': '',
                'first_level': '',
                'second_level': []

            }

            categories_dict['id'] = big_item.css('::attr("cid")').extract_first()
            categories_dict['key'] = big_item.css('::attr("cname")').extract_first().encode('utf-8')
            categories_dict['first_level'] = big_item.css('a::text').extract_first().encode('utf-8')
            if big_item.css('a::text').extract_first() == u'热门':
                continue
            find_item = str('div.tags_panel div.tag_wrap div[data-cache="' + big_item.css('::attr("cid")').extract_first() + '"]')
            categories_dict['second_level'] = response_panel.css(find_item).css('a::attr(tid)').extract()
            categories.append(categories_dict)

        for category in categories:
            if category['first_level'] in request_list:
                for second_level in category['second_level']:
                    yield scrapy.Request(
                        url='http://www.ximalaya.com/dq/{}-{}/1/'.format(category['key'], second_level.encode('utf-8')),
                        callback=self.parse_list,
                        meta={
                            'key': category['key'],
                            'first_level': category['first_level'],
                            'second_level': second_level.encode('utf-8')
                        }
                    )

    def parse_list(self, response):
        selector = Selector(response)
        for audio in selector.xpath('//div[@class="discoverAlbum_item"]'):
            info = XmlyInfoItem()
            info['first_level'] = response.meta.get('first_level')
            info['second_level'] = response.meta.get('second_level')
            info['url'] = response.request.url
            info['cover_pic'] = audio.xpath('.//img/@src').extract_first()
            info['play_count'] = audio.xpath(
                './/span[@class="sound_playcount"]//text()').extract_first()
            info['title'] = audio.xpath(
                './/a[@class="discoverAlbum_title"]//text()').extract_first().replace('"',"'")
            info['last_track'] = audio.xpath(
                './/a[@class="title"]//text()').extract_first() or ""
            info['last_track'] = info['last_track'].replace('"',"'")
            url = audio.xpath(
                './/a[@class="discoverAlbum_title"]/@href').extract_first()
            ids = re.findall(r'\d+', url)
            info['xmly_uploader_id'] = ids[0]
            info['xmly_album_id'] = ids[1]
            yield scrapy.Request(
                '{}?order=asc&page=1'.format(url),
                meta={
                    "item": info,
                    "order": 'asc',
                },
                callback=self.parse_detail
            )

        if selector.css('div.pagingBar_wrapper a[rel="next"]'):
            yield scrapy.Request(
                url=urlparse.urljoin(response.url, selector.css('div.pagingBar_wrapper a[rel="next"]::attr(href)').extract_first()),
                callback=self.parse_list,
                meta={
                    'first_level': response.meta.get('first_level'),
                    'second_level': response.meta.get('second_level')
                })

    def parse_detail(self, response):

        selector = Selector(response)
        info = response.meta.get('item')
        order = response.meta.get('order')

        # pages
        if 'page=1' == response.request.url[-6:]:
            info['intro'] = ''.join(selector.xpath('//div[@class="mid_intro"]/article//text()').extract(
            )).strip().encode('utf-8').translate(None, '\r\n\t"')
            yield info

            date_list = selector.xpath('//li[@sound_id]//div[@class="operate"]/span/text()').extract()
            date_list_sorted = sorted(date_list)  # 升序
            date_list_sorted_reversed = sorted(date_list, reverse=True)  # 降序

            if date_list[0] != date_list_sorted[0] and date_list[0] == date_list_sorted_reversed[0]:  # 不是升序， 是降序
                order = 'desc'
                yield scrapy.Request(
                    url=response.url.replace('asc', 'desc'),
                    meta={
                        "item": info,
                        "order": order
                    },
                    callback=self.parse_detail
                )
                return

        detail = XmlyDetailItem()
        detail['url'] = response.request.url
        detail['uploader'] = ''.join(selector.xpath(
            '//div[@class="username"]/text()').extract()).strip()
        detail['uploader_cover'] = selector.xpath(
            '//div[@class="picture"]//img/@src').extract_first()
        detail['title'] = selector.xpath(
            '//div[@class="detailContent_title"]//h1/text()').extract_first().replace('"', "'")
        detail['labels'] = '-'.join(selector.xpath(
            '//div[@class="tagBtnList"]//span/text()').extract()).replace('"', "'")
        detail['xmly_uploader_id'] = info['xmly_uploader_id']
        detail['xmly_album_id'] = info['xmly_album_id']
        detail['first_level'] = info['first_level']
        detail['second_level'] = info['second_level']
        page = selector.xpath('//a[@class="pagingBar_page on"]//text()').extract_first() or '1'
        base = (int(page)-1)*100
        for index, track in enumerate(selector.xpath('//li[@sound_id]')):
            detail['xmly_sound_id'] = track.xpath(
                './@sound_id').extract_first()
            detail['track_title'] = track.xpath(
                './/a[@class="title"]/@title').extract_first().replace('"', "'")
            detail['track_play_count'] = track.xpath(
                './/span[@class="sound_playcount"]/text()').extract_first()
            detail['track_upload_date'] = track.xpath(
                './/div[@class="operate"]/span/text()').extract_first()
            detail['track_in_album'] = base + index + 1
            yield detail

        if selector.css('div.pagingBar_wrapper a[rel="next"]'):
            yield scrapy.Request(
                url=urlparse.urljoin(response.url, selector.css('div.pagingBar_wrapper a[rel="next"]::attr(href)').extract_first()).replace('asc', order),
                callback=self.parse_detail,
                meta={
                    "item": info,
                    'order': order
                })
