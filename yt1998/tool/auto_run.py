# -*- coding:utf-8 -*-

'''

$ python run_spider.py  1
'''

import time
import os
import sys


if __name__ == '__main__':
    if not os.path.isdir('log'):
        os.system('rm -rf log')
        os.system('mkdir log')
    if not os.path.isdir('dailyresult'):
        os.system('mkdir dailyresult')

    process_num = int(sys.argv[1])
    spiders = ['', 'yaotong_news_add']
    for i in range(1, len(spiders)):
        ret_dir = 'dailyresult'.format(i)
        # if not os.path.exists(ret_dir):
        #    os.system('mkdir -p {}'.format(ret_dir))
        cmd = 'scrapy crawl {} --loglevel=INFO --logfile=log/{}.log -a result_dir={} &'.format(
            spiders[i], spiders[i], ret_dir)
        print 'Run: {}'.format(cmd)
        os.system(cmd)
        time.sleep(5)
    time.sleep(20)
    for i in range(1, len(spiders)):
        f = './result/' + spiders[i] + '.json'
        if os.path.exists(f):
            continue
        else:
            cmd = 'scrapy crawl {} --loglevel=INFO --logfile=log/{}.log -a result_dir={} &'.format(
                spiders[i], spiders[i], ret_dir)
            print 'reRun: {}'.format(cmd)
            os.system(cmd)
            time.sleep(5)
