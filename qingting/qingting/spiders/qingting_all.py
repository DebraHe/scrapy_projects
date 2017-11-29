# -*- coding: utf-8 -*-
import scrapy
from qingting.items import QingtingDetailItem
from tool.data import convert
from itertools import product
import json
import math

_META_VERSION = 'v1.0'


class QingtingDetailSpider(scrapy.Spider):
    name = 'qingting_all'
    meta_version = _META_VERSION
    result_dir = './result'
    category_url = 'http://api.open.qingting.fm/v6/media/categories/{}?access_token={}'
    channel_url = 'http://i.qingting.fm/capi/neo-channel-filter?category={}&attrs={}&curpage={}'
    search_url1 = 'http://api.open.qingting.fm/v6/media/channelondemands/{}?access_token={}'
    search_url2 = 'http://api.open.qingting.fm/v6/media/channelondemands/{}/programs/curpage/{}/pagesize/250?access_token={}'
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'ITEM_PIPELINES': {
            # 'qingting.pipelines.QingtingPipeline': 300,
            'qingting.pipelines.MongoDBPipleline': 301
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.http.FormRequest(
            url='http://api.open.qingting.fm/access?&grant_type=client_credentials',
            formdata={
                'client_id': 'XXX',
                'client_secret': 'XXX',
            },
            callback=self.parse_access_token
        )

    def parse_access_token(self, response):
        access_token = json.loads(response.text).get('access_token')
        categories = {
            3617: "精品内容",
            527: "相声小品",
            3251: "脱口秀",
            547: "娱乐",
            3252: "搞笑",
            537: "教育",
            1585: "公开课",
            3613: "文化",
            3496: "评书",
            3276: "戏曲",
            3636: "出版精品",
            1599: "儿童"
        }
        # 获取所有一级分类下的二级分类
        for category_id in categories.keys():
            yield scrapy.http.Request(
                url=self.category_url.format(category_id, access_token),
                callback=self.parse_category_ids,
                meta={
                    'access_token': access_token,
                    'category_id': category_id
                }
            )

    def parse_category_ids(self, response):
        access_token = response.meta.get('access_token')
        category_id = response.meta.get('category_id')
        data = json.loads(response.text).get('data', [])
        attrs = list(product(*[group.get('values', []) for group in data]))
        for attr in attrs:
            attr_ids = '-'.join([str(i['id']) for i in list(attr)])
            yield scrapy.http.Request(
                url=self.channel_url.format(category_id, attr_ids, 1),
                callback=self.parse_list,
                meta={
                    'access_token': access_token,
                    'category_id': category_id,
                    'attr_ids': attr_ids,
                }
            )

    def parse_list(self, response):
        access_token = response.meta.get('access_token')
        category_id = response.meta.get('category_id')
        attr_ids = response.meta.get('attr_ids')
        total = json.loads(response.text).get('total')
        if total:
            datas = json.loads(response.text).get('data').get('channels')
            for data in datas:
                qingting_channel_id = data.get('id')
                url = self.search_url1.format(qingting_channel_id, access_token)
                yield scrapy.http.Request(
                    url=url,
                    meta={
                        'access_token': access_token
                    },
                    callback=self.parse_detail)

            for i in range(1, int(math.ceil(total / 12.0))):
                yield scrapy.http.Request(
                    url=self.channel_url.format(category_id, attr_ids, 1),
                    callback=self.parse_list,
                    meta={
                        'access_token': access_token,
                        'category_id': category_id,
                        'attr_ids': attr_ids,
                    }
                )

    def parse_detail(self, response):
        access_token = response.meta.get('access_token')
        json_data = json.loads(response.text)
        item = QingtingDetailItem()
        if json_data.get('data'):
            item['title'] = json_data['data']['title']
            item['anchor_name'] = json_data['data']['detail']['podcasters'][0]['nickname'] if json_data['data']['detail']['podcasters'] else ''
            item['anchor_cover_pic'] = json_data['data']['thumbs']['200_thumb']
            item['qingting_channel_id'] = int(json_data['data']['id'])
            item['last_update'] = json_data['data']['update_time']
            item['tracks'] = int(json_data['data']['detail']['program_count'])
        # 每页上限250
        for i in range(int(math.ceil(item['tracks'] / 250.0))):
            yield scrapy.http.Request(
                url=self.search_url2.format(item['qingting_channel_id'], str(i + 1), access_token),
                meta={'item': item},
                callback=self.parse_track)

    def parse_track(self, response):
        json_data = json.loads(response.text)
        for track in json_data['data']:
            item = QingtingDetailItem()
            item.update(response.meta['item'])
            item['track_title'] = track['title']
            item['play_time'] = track['duration']
            item['update_time'] = track['update_time']
            item['qingting_programs_id'] = int(track['id'])
            item['url'] = track['weburl']
            item['mediainfo'] = convert(track['mediainfo'])
            json.loads(json.dumps(track['mediainfo']).encode('utf-8'))
            yield scrapy.http.Request(
                url='http://www.qingting.fm/channels/{}/programs/{}'.format(
                    item['qingting_channel_id'], item['qingting_programs_id']),
                meta={'item': item},
                callback=self.parse_count)

    def parse_count(self, response):
        # 播放量
        item = response.meta['item']
        item['play_count'] = response.xpath(
            '//span[@class="exwk SgGn"]/preceding-sibling::span[not(@class)]/text()').extract_first()
        yield item