# -*- coding: utf-8 -*-

import json
import scrapy
from music163.items import LyricItem

_META_VERSION = 'v1.0'


class Music163LyricSpider(scrapy.Spider):
    name = "music163_lyric"
    result_dir = './result'
    meta_version = _META_VERSION
    # settings
    custom_settings = {
        'ITEM_PIPELINES': {
            'music163.pipelines.LyricPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        with open('doc/song_ids.txt') as f:
            for songid in f.readlines():
                song_id = str(songid.strip())
                lyric_api = 'http://music.163.com/api/song/media?id='
                yield scrapy.http.Request(
                    url=lyric_api + song_id,
                    meta={'song_id': song_id}
                )

    def parse(self, response):
        item = LyricItem()
        item['url'] = response.url
        item['id'] = response.meta.get('song_id')
        lyric = json.loads(response.text).get('lyric')
        if lyric:
            item['raw_lyric'] = lyric
            yield item