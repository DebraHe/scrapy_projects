# -*- coding:utf-8 -*-


import codecs
import json


def main():
    ret = {}
    with open('result/tianyancha_list.json') as f:
        for _ in f.readlines():
            d = json.loads(_.strip())
            pinyin = d.get('download_data').get('parsed_data').get('pinyin')
            word = d.get('download_data').get('parsed_data').get('word')
            expression = d.get('download_data').get('parsed_data').get('expression')
            if word not in ret:
                ret[word] = u'{},{},{}'.format(pinyin, word, expression).encode('utf8')
    with codecs.open('result/result.csv', 'w') as f:
        f.write('\n'.join(ret.values()))


if __name__ == '__main__':
    main()
