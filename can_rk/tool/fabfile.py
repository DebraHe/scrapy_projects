# -*- coding: utf-8 -*-
from fabric.api import *

env.hosts = [
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

@parallel
def run_spider():
    cmd = 'python tool/run_spider.py wenshu_detail 1'
    with cd('/home/ubuntu/can_rk'):
        run(cmd, pty=False)


@parallel
def check():
    # cmd = 'ps ax|grep python'
    # cmd = 'wc -l doc/code_failed2.txt'
    # cmd = 'wc -l doc/failed_name3.txt'
    # cmd = 'wc -l doc/succeed_name3.txt'
    # cmd = 'wc -l doc/person_id.txt'
    # cmd = 'wc -l result/*/*'
    # cmd = 'wc -l doc/failed_name3.txt'
    # cmd = 'sudo pip install pillow'
    cmd = 'tail -n 5 log/*'
    # cmd = 'grep httperror log/*'
    # cmd = 'grep ERROR log/*'
    # cmd = 'rm -r -f log/'
    # cmd = 'ls'
    with cd('/home/ubuntu/can_rk'):
        run(cmd)


@parallel
def stop():
    with settings(warn_only=True):
        run("ps ax|grep python | awk '{print $1}'| xargs kill -9")
