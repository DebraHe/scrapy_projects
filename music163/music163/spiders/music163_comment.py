# -*- coding: utf-8 -*-

import json
import scrapy
from music163.items import CommentItem
from tool.tool import get_encSecKey, get_params
_META_VERSION = 'v1.0'


class Music163CommentSpider(scrapy.Spider):
    name = "music163_comment"
    result_dir = './result'
    meta_version = _META_VERSION
    # settings
    custom_settings = {
        'ITEM_PIPELINES': {
            'music163.pipelines.CommentPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        with open('doc/song_ids.txt') as f:
            for songid in f.readlines():
                song_id = str(songid.strip())
                formdata = {
                    "params": get_params(1),
                    "encSecKey": get_encSecKey()
                }
                yield scrapy.http.FormRequest(
                    url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token='.format(song_id),
                    formdata=formdata,
                    meta={'song_id': song_id}
                )

    def parse(self, response):
        item = CommentItem()
        item['url'] = response.url
        song_id = response.meta.get('song_id')
        item['id'] = song_id
        comment_json = json.loads(response.text)
        if comment_json.get('comments'):
            for comment in comment_json.get('comments'):
                item['user_name'] = comment.get('user').get('nickname')
                item['content'] = comment.get('content')
                item['com_time'] = comment.get('time')
                item['praise_num'] = comment.get('likedCount')
                yield item

            # 下一页
            comments_num = int(comment_json['total'])
            if comments_num % 20 == 0:
                page = comments_num / 20
            else:
                page = int(comments_num / 20) + 1
            if page != 1:
                for p in range(2, page):
                    formdata = {
                        "params": get_params(p),
                        "encSecKey": get_encSecKey()
                    }
                    yield scrapy.http.FormRequest(
                        url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token='.format(song_id),
                        formdata=formdata,
                        meta={'song_id': song_id}
                    )