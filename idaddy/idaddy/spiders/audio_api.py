# -*- coding: utf-8 -*-
import scrapy
from idaddy.items import IdaddyDetailItem
from tool.tool import get_nonce, get_timestamp, get_signature
import json
from tool.data import clean
_META_VERSION = 'v1.0'
timestamp = get_timestamp()


class AudioSpider(scrapy.Spider):
    name = "audio_api"
    app_id = 'haizhi0000000001'
    host = 'http://ilisten.idaddy.cn'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'ITEM_PIPELINES': {
            # 'idaddy.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        with open('doc/cat_ids.txt') as f:
            for cat_id in f.readlines():
                yield scrapy.http.FormRequest(
                    url='http://open.idaddy.cn/audio/v2/list?',
                    formdata={
                        'app_id': self.app_id,
                        'device_id': '12',
                        'timestamp': timestamp,
                        'nonce': get_nonce(),
                        'signature': get_signature(self.app_id, timestamp),
                        'cat_ids': '[{}]'.format(cat_id),
                        'chapter': '1',
                        'verbose': '0',
                        'offset': '0',
                        'limit': '99'
                    },
                    callback=self.parse_list,
                    meta={'offset': 0, 'cat_id': cat_id}
                )

    def parse_list(self, response):
        data = json.loads(response.text)['audioinfos']['contents']
        if len(data) == 0:
            self.logger.info(response.meta.get('cat_id').strip())
            self.logger.info(json.loads(response.text))
            return
        content_ids = []
        for item in data:
            content_ids.append('"{}"'.format(item['id']))
        for i in range(0, len(content_ids), 20):
            yield scrapy.http.FormRequest(
                url='http://open.idaddy.cn/audio/v2/query?',
                formdata={
                    'app_id': self.app_id,
                    'device_id': '12',
                    'timestamp': timestamp,
                    'nonce': get_nonce(),
                    'signature': get_signature(self.app_id, timestamp),
                    'content_ids': '[{}]'.format(','.join(content_ids[i:i+20])),
                    'verbose': '1',
                },
                callback=self.parse_detail
            )

        # next page
        offset = response.meta.get('offset') + len(data)
        cat_id = response.meta.get('cat_id')
        yield scrapy.http.FormRequest(
            url='http://open.idaddy.cn/audio/v2/list?',
            formdata={
                'app_id': self.app_id,
                'device_id': '12',
                'timestamp': timestamp,
                'nonce': get_nonce(),
                'signature': get_signature(self.app_id, timestamp),
                'cat_ids': '[{}]'.format(cat_id),
                'chapter': '1',
                'verbose': '0',
                'offset': str(offset),
                'limit': '99'
            },
            callback=self.parse_list,
            meta={'offset': offset, 'cat_id': cat_id}
        )

    def parse_detail(self, response):
        data = json.loads(response.text)['audioinfos']['contents']
        if len(data) == 0:
            self.logger.info('====', json.loads(response.text))
        for song in data:
            item = IdaddyDetailItem()
            item['url'] = response.request.url
            item['cats'] = song['cats']
            item['first_level'] = ''
            item['second_level'] = ''
            item['title'] = clean(song['name'])
            item['episodes'] = song['chapter_count']
            item['intro'] = clean(song['description'])
            item['rating_number'] = ''
            if song['has_chapter'] == 0:
                # 单曲
                item['album_id'] = song['id']
                item['chapter_id'] = ''
                item['track_in_albun'] = ''
                item['track_title'] = ''
                item['play_time'] = song['duration']
                item['Type'] = 'single'
                yield item
            else:
                # 专辑
                for track in song['chapters']:
                    item['chapter_id'] = track['chapter_id']
                    item['album_id'] = song['id']
                    item['track_in_albun'] = track['order_no']
                    item['track_title'] = clean(track['name'])
                    item['play_time'] = track['duration']
                    item['Type'] = 'album'
                    yield item
