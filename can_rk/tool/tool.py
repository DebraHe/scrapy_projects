# -*- coding:utf-8 -*-
import os
import random
import urllib

import requests
from PIL import Image, ImageEnhance
from io import BytesIO

from rk import RClient


def get_phantomjs():
    return '/Users/debrahe/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'


def get_img(left, right, up, down):
    left = int(left)
    right = int(right)
    up = int(up)
    down = int(down)
    im = Image.open('code.jpg')
    im = im.crop((left, up, right, down))
    im = im.convert('L')
    sharpness = ImageEnhance.Contrast(im)
    sharper_im = sharpness.enhance(2.0)
    sharper_im.save('code.jpg')
    with open('code.jpg', 'rb') as f:
        res = f.read()
    return res


def get_code():
    captchaId = ''.join(random.sample('0123456789abcdef0123456789abcdef', 32))
    rc = RClient('XXX', 'XXX', 'XXX', 'XXX')
    code = ''
    while code == '':
        try:
            img_url = 'http://zhixing.court.gov.cn/search/captcha.do?captchaId={}&random=0.4750974032186893'.format(captchaId)
            urllib.urlretrieve(img_url, 'code.jpg')
            with open('code.jpg', 'rb') as f:
                res = f.read()
                os.remove('code.jpg')
                code = rc.rk_create(res, 2040)['Result']
        except:
            pass
    return captchaId, code


def get_code_shixin():
    captchaId = ''.join(random.sample('0123456789abcdef0123456789abcdef', 32))
    rc = RClient('XXX', 'XXX', 'XXX', 'XXX')
    code = ''
    while code == '':
        try:
            img_url = 'http://shixin.court.gov.cn/captchaNew.do?captchaId={}&random=0.23790190675874312'.format(captchaId)
            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))
            try:
                r, g, b, a = image.split()
            except:
                r, g, b = image.split()
            im = Image.merge("RGB", (r, g, b))
            im.save('code2.jpg')
            with open('code2.jpg', 'rb') as f:
                res = f.read()
                os.remove('code2.jpg')
                code = rc.rk_create(res, 2040)['Result']
        except:
            pass
    return captchaId, code
