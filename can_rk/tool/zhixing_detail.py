# -*- coding: utf-8 -*-

'''
命令：
$ python set_start_urls REDIS_KEY
#################################################
设置豆瓣初始url：
$ python set_start_urls douban_detail:start_urls
失败请求重爬
$ python set_start_urls douban_detail_failed:start_urls
'''

import redis


def set_start_urls(redis_key):
    r = redis.Redis(host='10.9.161.8', port=6379)
    with open('../doc/person_id.txt') as f:
        pnames = [line.strip() for line in f.readlines()]
    for pname in pnames:
        r.lpush(redis_key, pname)


if __name__ == '__main__':
    try:
        redis_key = 'zhixing_detail:start_urls'
        print 'set redis key: {}'.format(redis_key)
        set_start_urls(redis_key)
    except:
        print __doc__
