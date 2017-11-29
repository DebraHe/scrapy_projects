# -*- coding:utf-8 -*-
import json


def get_detail_url():
    with open('../result/tianyancha_list.json') as f:
        for s in f.readlines():
            print json.loads(s).get('download_data').get('parsed_data').get('item_url')


if __name__ == '__main__':
    get_detail_url()
