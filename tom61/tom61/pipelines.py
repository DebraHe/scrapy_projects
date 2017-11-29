# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

from tool.tool import unicode_to_str


class ShiwangeweishenmePipeline(object):
    def process_item(self, item, spider):
        filename = 'shiwangeweishenme.json'
        result_dir = spider.result_dir
        result = {
            'meta_version': spider.meta_version,
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': '',
                'method': 'GET',
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }
        result['download_config']['url'] = unicode_to_str(item['url'])

        result['download_data']['parsed_data'][
            'title'] = unicode_to_str(item['title'])
        result['download_data']['parsed_data'][
            'label'] = unicode_to_str(item['label'])
        result['download_data']['parsed_data'][
            'data_time'] = unicode_to_str(item['data_time'])
        result['download_data']['parsed_data'][
            'description'] = unicode_to_str(item['description'])

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        return item
