# -*- coding:utf-8 -*-

'''
开启10个进程跑 xiami_all_dist 爬虫
$ python run_spider xiami_all_dist 10
'''

import time
import os
import sys


if __name__ == '__main__':
    if not os.path.isdir('log'):
        os.system('rm -rf log')
        os.system('mkdir log')

    if not os.path.isdir('result'):
        os.system('mkdir result')

    spider = sys.argv[1]
    process_num = int(sys.argv[2])

    for i in range(1, process_num + 1):
        ret_dir = 'result/ret{}'.format(i)
        if not os.path.exists(ret_dir):
            os.system('mkdir -p {}'.format(ret_dir))
        cmd = 'scrapy crawl {} --loglevel=INFO --logfile=log/{}.log -a result_dir={} &'.format(
            spider, i, ret_dir)
        print 'Run: {}'.format(cmd)
        os.system(cmd)
        time.sleep(3)
