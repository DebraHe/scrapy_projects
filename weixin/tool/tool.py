# -*- coding: utf-8 -*-
import datetime
import time
from PIL import Image, ImageEnhance

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def end_day():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    ISOFOMAT = "%Y-%m-%d"
    return today.strftime(ISOFOMAT)


def start_day():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    ISOFOMAT = "%Y-%m-%d"
    return yesterday.strftime(ISOFOMAT)


def get_today():
    today = datetime.date.today()
    ISOFOMAT = "%Y年%-m月%-d日"
    # return "2017年6月25日".decode('utf-8')
    return today.strftime(ISOFOMAT)


def get_phantomjs():
    return '/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'


# def get_phantomjs():
#     return '/Users/debrahe/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'


def get_proxy():
    try:
        # 代理服务器
        proxyHost = "proxy.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "XXX"
        proxyPass = "XXX"

        service_args = [
            "--proxy-type=http",
            "--proxy=%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
            },
            "--proxy-auth=%(user)s:%(pass)s" % {
                "user": proxyUser,
                "pass": proxyPass,
            },
        ]
        return service_args

    except:
        print 'Cannot get any proxy!'
        time.sleep(60)
        return get_proxy()


def get_img(left, right, up, down):
    left = int(left)
    right = int(right)
    up = int(up)
    down = int(down)
    im = Image.open('code_2.jpg')
    im = im.crop((left, up, right, down))
    im = im.convert('L')
    sharpness = ImageEnhance.Contrast(im)
    sharper_im = sharpness.enhance(2.0)
    sharper_im.save('code_2.jpg')
    with open('code_2.jpg', 'rb') as f:
        res = f.read()
    return res