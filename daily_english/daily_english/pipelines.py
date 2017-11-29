# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DailyEnglishPipeline(object):
    def process_item(self, item, spider):
        filename = 'result.json'
        result_dir = spider.result_dir
        result = {
            'meta_version': spider.meta_version,
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': item['url'],
                'method': 'GET',
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }

        result['download_data']['parsed_data'][
            'english'] = item['english']
        result['download_data']['parsed_data'][
            'chinese'] = item['chinese']

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        return item
