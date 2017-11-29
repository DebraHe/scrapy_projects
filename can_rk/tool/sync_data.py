# -*- coding: utf-8 -*-

import os
hosts = [
    'ubuntu@106.75.92.218',
    'ubuntu@106.75.97.244',
    'ubuntu@106.75.97.154',
    'ubuntu@106.75.98.168',
    'ubuntu@106.75.104.214',
    'ubuntu@106.75.97.184',
    'ubuntu@106.75.98.24',
    'ubuntu@106.75.97.198',
    'ubuntu@106.75.97.190',
    'ubuntu@106.75.104.181',
]


def sync_data():
    for h in hosts:
        cmd = 'rsync -rz {}:/home/ubuntu/can_rk/result/ /Users/debrahe/Desktop/result/{}-result/ \n'.format(
            h, h)
        # cmd = 'rsync -rz {}:/home/ubuntu/can_rk/doc/ /Users/debrahe/Desktop/result/{}-doc/ \n'.format(
        #     h, h)
        # cmd = 'scp /Users/debrahe/Desktop/can_rk/can_rk/spiders/wenshu_detail.py {}:/home/ubuntu/can_rk/can_rk/spiders/ \n'.format(
        #     h, h)
        print cmd
        os.system(cmd)


if __name__ == '__main__':
    sync_data()
