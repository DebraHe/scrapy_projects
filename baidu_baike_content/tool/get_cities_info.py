# -*- coding: utf-8 -*-

import json
import re
from scrapy.selector import Selector

RESULT_FILE = 'cities.json'


def merge():
    result = []
    with open(RESULT_FILE) as f:
        lines = f.readlines()
    for line in lines:
        try:
            d = {}
            s = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_page_content')   # 读取页面HTML
            response = Selector(text=s)

            # 获取所有结构化数据
            s = response.css('div.basic-info dl.basicInfo-left dt.name::text').extract()
            # tbl_keys = sel.xpath('//dl/dt/text()').extract()
            # tbl_contents = sel.xpath('//dl/dd').extract()
            # for i, k in enumerate(tbl_keys):
            #     k = ''.join(k.strip().split())
            #     s = re.sub(r'<.*?>', '', tbl_contents[i])
            #     s = ''.join(s.strip().split())
            #     d[k] = s
            # result.append(d)
        except:
            print 'Json parsing error: {}'.format(line)
            continue
    return result

if __name__ == '__main__':
    l = merge()
    for _ in l:
        for k, v in _.items():
            print '{}: {}'.format(k.encode('utf8'), v.encode('utf8'))
        print
