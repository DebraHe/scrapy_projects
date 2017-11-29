# -*- coding:utf-8 -*-


import codecs
import json

import re


def main():
    ret = {}
    with open('result/shiwangeweishenme.json') as f:
        for _ in f.readlines():
            d = json.loads(_.strip())
            title = d.get('download_data').get('parsed_data').get('title')
            label = d.get('download_data').get('parsed_data').get('label')
            data_time = d.get('download_data').get('parsed_data').get('data_time')
            description = re.sub(r'\s', '', d.get('download_data').get('parsed_data').get('description'))
            if title not in ret:
                ret[title] = u'{},{},{},{}'.format(title, label, data_time, description).encode('utf8')
    with codecs.open('result/result.csv', 'w') as f:
        f.write('\n'.join(ret.values()))


if __name__ == '__main__':
    main()
